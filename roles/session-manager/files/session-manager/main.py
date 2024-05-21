import os
import random
import requests
import memcache
import json
from flask import Flask, request, jsonify
from datetime import datetime
from access_guacamole import (
    generate_auth_token,
    get_user,
    create_connection,
    assign_user_to_connection,
    get_connection_info,
    get_connection_params,
    get_work_from_identifier,
)
from access_docker import create_service
from access_swl import open_port
from access_idm import get_swczone

app = Flask(__name__)

GUAC_DATABASE = os.environ.get("GUAC_DATABASE")
MEMCACHED_URL = os.environ.get("MEMCACHED_URL")
SW_LISTENER = os.environ.get("SW_LISTENER")
UNAVAILABLE_PORTS = os.environ.get("UNAVAILABLE_PORTS")


def check_worker_permissions(username, work):
    if not (work["isWorker"] or username == "guacadmin"):
        raise Exception("The specified user is not registered as a worker.")


def check_working_hours(username, work):
    ok_flag = False
    today = datetime.today().date()
    time = datetime.now().time()
    for period in work["periods"]:
        valid_from_date = datetime.strptime(period["validFrom"], "%Y-%m-%d").date()
        valid_until_date = datetime.strptime(period["validUntil"], "%Y-%m-%d").date()
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


def create_guacamole_connection(
    auth_token, work_id, info, params, username, identifier
):
    if "swcZone" not in params:
        if info["protocol"] == "vnc":
            status_msg = "Successfully Created"
            work_container = create_service(
                app.logger, work_id, params["httpLoginFormat"]
            )
            result_create_connection = create_connection(
                token=auth_token,
                database=GUAC_DATABASE,
                info=info,
                params=params,
                type="changepw" if work_id == "changepw" else "session-manager-chrome",
                hostname=work_container,
                port=os.environ.get("VNC_PORT"),
                origin_identifier=identifier,
                password=os.environ.get("VNC_PASSWORD"),
            )
            assign_user_to_connection(
                auth_token,
                GUAC_DATABASE,
                username,
                result_create_connection["identifier"],
            )
            app.logger.info(
                f"{work_container}: Create VNC connection object to guacamole successfully"
            )
            res_id = result_create_connection["identifier"]
        else:
            status_msg = "Already Created"
            res_id = identifier
    else:
        mc = memcache.Client([MEMCACHED_URL])
        if mc.get(f"{work_id}|{identifier}") == None:
            status_msg = "Successfully Created"
            swczone = get_swczone(params["swcZone"])
            uid = random.choice(swczone["swConnector"])
            ports = mc.get("ports") or ()
            items = UNAVAILABLE_PORTS.split(",")
            unavailable_ports = tuple(items)
            available_ports = [
                port
                for port in range(1025, 65536)
                if port not in ports + unavailable_ports
            ]
            random_port = random.choice(available_ports)
            res = open_port(uid, random_port, params["hostname"], int(params["port"]))
            if res.status_code != requests.codes.ok:
                raise Exception("Failed to open port for sw-listener: {}", random_port)
            app.logger.info("Succeeded to open port for sw-listener: {}", random_port)
            mc.append("ports", random_port)
            response_generate_auth_token = generate_auth_token()
            auth_token = response_generate_auth_token["authToken"]
            result_create_connection = create_connection(
                token=auth_token,
                database=GUAC_DATABASE,
                info=info,
                params=params,
                type="changepw" if work_id == "changepw" else "session-manager",
                hostname=SW_LISTENER,
                port=random_port,
                origin_identifier=identifier,
            )
            assign_user_to_connection(
                auth_token,
                GUAC_DATABASE,
                username,
                result_create_connection["identifier"],
            )
            app.logger.info("Create connection object to guacamole successfully")
            key = f"{work_id}|{identifier}"
            keys = mc.get("all_keys") or []
            if key not in keys:
                keys.append(key)
                mc.set("all_keys", keys)
            mc.set(key, result_create_connection["identifier"])
            res_id = result_create_connection["identifier"]
        else:
            status_msg = "Already Created"
            res_id = mc.get(f"{work_id}|{identifier}")
        if info["protocol"] == "vnc":
            status_msg = "Successfully Created"
            swl_info = get_connection_info(auth_token, GUAC_DATABASE, res_id)
            swl_params = get_connection_params(auth_token, GUAC_DATABASE, res_id)
            swl_httpLoginFormat:dict = json.loads(swl_params["httpLoginFormat"])
            swl_httpLoginFormat.update({
                "fqdn": f"{swl_params["hostname"]}:{swl_params["port"]}"
            })
            swl_params["httpLoginFormat"] = json.dumps(swl_httpLoginFormat)
            work_container = create_service(
                app.logger, work_id, json.dumps(swl_httpLoginFormat)
            )
            result_vnc_create_connection = create_connection(
                token=auth_token,
                database=GUAC_DATABASE,
                info=swl_info,
                params=swl_params,
                type="changepw" if work_id == "changepw" else "session-manager-chrome",
                hostname=work_container,
                port=os.environ.get("VNC_PORT"),
                origin_identifier=res_id,
                password=os.environ.get("VNC_PASSWORD"),
            )
            assign_user_to_connection(
                auth_token,
                GUAC_DATABASE,
                username,
                result_vnc_create_connection["identifier"],
            )
            app.logger.info(
                f"{work_container}: Create VNC connection object to guacamole successfully"
            )
            res_id = result_vnc_create_connection["identifier"]
    return jsonify(
        {
            "status": status_msg,
            "identifier": res_id,
        }
    )


@app.route("/create", methods=["POST"])
def create():
    try:
        work_id = str(request.json["work_id"])
        worker_token = str(request.json["worker_token"])
        identifier = str(request.json["identifier"])

        response_generate_auth_token = generate_auth_token()
        auth_token = response_generate_auth_token["authToken"]

        user = get_user(worker_token)
        username = user["username"]
        work = get_work_from_identifier(worker_token, GUAC_DATABASE, work_id)
        info = get_connection_info(auth_token, GUAC_DATABASE, identifier)
        params = get_connection_params(auth_token, GUAC_DATABASE, identifier)

        check_worker_permissions(username, work)
        check_working_hours(username, work)

        return create_guacamole_connection(
            auth_token, work_id, info, params, username, identifier
        )

    except Exception as e:
        app.logger.exception(e)
        return jsonify({"error_message": str(e)}), 500
