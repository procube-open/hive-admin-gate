import os
import random
import requests
import memcache
from flask import Flask, request, jsonify
from datetime import datetime
from access_guacamole import get_user
from access_docker import create_service, delete_service
from access_swl import open_port
from access_idm import get_swczone
from access_guacamole import (
    generate_auth_token,
    create_connection,
    delete_connection,
    assign_user_to_connection,
    get_connection_info,
    get_connection_params,
    get_work_from_identifier,
)

app = Flask(__name__)


# body format
# {
#     "work_id": str,
#     "worker_token": str,
#     "identifier": str,
# }
@app.route("/create", methods=["POST"])
def create():
    try:
        # JSON取得
        work_id = str(request.json["work_id"])
        worker_token = str(request.json["worker_token"])
        identifier = str(request.json["identifier"])

        # 環境変数取得
        memcached_url = os.environ.get("MEMCACHED_URL")
        sw_listener = os.environ.get("SW_LISTENER")
        unavailable_ports = os.environ.get("UNAVAILABLE_PORTS")
        guac_database = os.environ.get("GUAC_DATABASE")
        
        # authトークン生成
        response_generate_auth_token = generate_auth_token()
        auth_token = response_generate_auth_token["authToken"]
        
        # 情報取得 
        user = get_user(worker_token)
        username = user["username"]
        work = get_work_from_identifier(worker_token, guac_database, work_id)
        info = get_connection_info(auth_token, guac_database, identifier)
        params = get_connection_params(auth_token, guac_database, identifier)

        # 作業者確認
        if not (work["isWorker"] or username == "guacadmin"):
            raise Exception("The specified user is not registered as a worker.")

        # 作業時間確認
        ok_flag: bool = False
        today = datetime.today().date()
        time = datetime.now().time()
        for period in work["periods"]:
            valid_from_date = datetime.strptime(period["validFrom"], "%Y-%m-%d").date()
            valid_until_date = datetime.strptime(
                period["validUntil"], "%Y-%m-%d"
            ).date()
            start_time = datetime.strptime(period["startTime"], "%H:%M:%S").time()
            end_time = datetime.strptime(period["endTime"], "%H:%M:%S").time()
            if (
                valid_from_date <= today
                and valid_until_date >= today
                and start_time <= time
                and end_time >= time
            ):
                ok_flag = True
                break
        if not (ok_flag or username == "guacadmin"):
            raise Exception("Worker cannot connect outside of working hours.")

        # SW利用確認
        if "swcZone" not in params:
            if info["protocol"] == "vnc":
                # サービス作成
                http_login_format = params["httpLoginFormat"]
                work_container = create_service(app.logger, work_id, http_login_format)

                # guacamole 接続オブジェクト作成
                vnc_port = os.environ.get("VNC_PORT")
                vnc_password = os.environ.get("VNC_PASSWORD")
                result_create_vnc_connection = create_connection(
                    token=auth_token,
                    database=guac_database,
                    work_id=work_id,
                    protocol=info["protocol"],
                    hostname=work_container,
                    port=vnc_port,
                    username=None,
                    password=vnc_password,
                    httpLoginFormat=http_login_format,
                    originIdentifier=identifier,
                )

                # 接続権限付与
                assign_user_to_connection(
                    auth_token,
                    guac_database,
                    username,
                    result_create_vnc_connection["identifier"],
                )
                app.logger.info(
                    work_container
                    + ": Create VNC connection object to guacamole successfully"
                )

                return jsonify(
                    {
                        "status": "Successfully Created",
                        "work_id": work_id,
                        "work_container": work_container,
                        "identifier": result_create_vnc_connection["identifier"],
                        "info": result_create_vnc_connection,
                    }
                )
            else:
                return jsonify({"identifier": info["identifier"], "info": info})
        else:
            mc = memcache.Client([memcached_url])
            if mc.get(work_id + ":" + identifier) == None:
                swczone = get_swczone(params["swcZone"])
                uid = random.choice(swczone["swConnector"])
                if mc.get("ports") is None:
                    ports = ()
                else:
                    ports = mc.get("ports")
                items = unavailable_ports.split(",")
                unavailable_ports = tuple(items)
                available_ports = [
                    port
                    for port in range(1025, 65536)
                    if port not in ports + unavailable_ports
                ]
                random_port = random.choice(available_ports)
                # ポート開設
                res = open_port(uid, random_port, params["hostname"], int(params["port"]))
                if res.status_code != requests.codes.ok:
                    raise Exception("Failed to open port for sw-listener")

                app.logger.info("Succeeded to open port for sw-listener")
                mc.append("ports", random_port)

                if info["protocol"] == "vnc":
                    print("ng")
                else:
                    # authトークン生成
                    response_generate_auth_token = generate_auth_token()
                    auth_token = response_generate_auth_token["authToken"]

                    result_create_connection = create_connection(
                        token=auth_token,
                        database=guac_database,
                        work_id=work_id,
                        protocol=info["protocol"],
                        hostname=sw_listener,
                        port=random_port,
                        username=params["username"],
                        password=params["password"],
                        httpLoginFormat=None,
                        originIdentifier=identifier,
                    )
                    # 接続権限付与
                    assign_user_to_connection(
                        auth_token,
                        guac_database,
                        username,
                        result_create_connection["identifier"],
                    )
                    app.logger.info(
                        "Create connection object to guacamole successfully"
                    )
                    mc.set(work_id + ":" + identifier, result_create_connection["identifier"])
                    
                    return jsonify(
                        {
                            "status": "Successfully Created",
                            "work_id": work_id,
                            "identifier": result_create_connection["identifier"],
                            "info": result_create_connection,
                        }
                    )
            else:
                swl_identifier = mc.get(work_id + ":" + identifier)
                return jsonify(
                    {
                        "status": "Already Created",
                        "work_id": work_id,
                        "identifier": swl_identifier,
                        "info": get_connection_info(auth_token, guac_database, swl_identifier),
                    }
                )

    except Exception as e:
        app.logger.exception(e)
        return jsonify({"error_message": str(e)}), 500


# body format
# {
#     "work_container": str,
#     "identifier": str,
# }
@app.route("/delete", methods=["POST"])
def delete():
    try:
        # JSON取得
        work_container = request.json["work_container"]
        identifier = request.json["identifier"]
        guac_database = os.environ.get("GUAC_DATABASE")

        # authトークン生成
        response_generate_auth_token = generate_auth_token()
        auth_token = response_generate_auth_token["authToken"]

        # サービス削除
        delete_service(app.logger, work_container)

        # guacamole接続オブジェクト削除
        delete_connection(auth_token, guac_database, identifier)

        return jsonify(
            {"status": "Successfully Deleted", "work_container": work_container}
        )
    except Exception as e:
        app.logger.exception(e)
        return jsonify({"error_message": str(e)}), 500
