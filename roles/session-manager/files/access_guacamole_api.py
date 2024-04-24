import json
import os
import requests
import urllib

guacamole_url = os.environ.get("GUACAMOLE_URL")


def generate_auth_token():
    generate_auth_token_path = "/api/tokens"
    generate_auth_token_url = guacamole_url + generate_auth_token_path

    username = os.environ.get("GUACAMOLE_USERNAME")
    password = os.environ.get("GUACAMOLE_PASSWORD")
    params = {"username": username, "password": password}
    params = urllib.parse.urlencode(params)

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(generate_auth_token_url, data=params, headers=headers)
    return response.json()


def create_vnc_connection(work_container, work_id):
    response_generate_auth_token = generate_auth_token()
    auth_token = response_generate_auth_token["authToken"]
    guacamole_database = response_generate_auth_token["dataSource"]
    create_vnc_connection_path = (
        "/api/session/data/" + guacamole_database + "/connections?token=" + auth_token
    )
    create_vnc_connection_url = guacamole_url + create_vnc_connection_path

    vnc_port = os.environ.get("VNC_PORT")
    vnc_password = os.environ.get("VNC_PASSWORD")
    params = {
        "name": work_container,
        "parentIdentifier": "ROOT",
        "protocol": "vnc",
        "idmIdentifier": "changepw" if work_id == "changepw" else "session-manager",
        "parameters": {
            "hostname": work_container,
            "port": vnc_port,
            "password": vnc_password,
        },
        "attributes": {
            "guacd-encryption": "",
            "failover-only": "",
            "weight": "",
            "remark": "",
            "max-connections": "10",
            "guacd-hostname": "",
            "guacd-port": "",
            "max-connections-per-user": "10",
        },
    }
    params = json.dumps(params)

    headers = {"Content-Type": "application/json"}

    response = requests.post(create_vnc_connection_url, data=params, headers=headers)
    return response.json()


def delete_vnc_connection(vnc_identifier):
    response_generate_auth_token = generate_auth_token()
    auth_token = response_generate_auth_token["authToken"]
    guacamole_database = response_generate_auth_token["dataSource"]
    delete_vnc_connection_path = (
        "/api/session/data/"
        + guacamole_database
        + "/connections/"
        + vnc_identifier
        + "?token="
        + auth_token
    )
    delete_vnc_connection_url = guacamole_url + delete_vnc_connection_path

    headers = {"Content-Type": "application/json"}

    response = requests.delete(delete_vnc_connection_url, headers=headers)
    return response.status_code


def assign_user_to_connection(work_user, vnc_identifier):
    response_generate_auth_token = generate_auth_token()
    auth_token = response_generate_auth_token["authToken"]
    guacamole_database = response_generate_auth_token["dataSource"]
    assign_user_to_connection_path = (
        "/api/session/data/"
        + guacamole_database
        + "/users/"
        + work_user
        + "/permissions"
    )
    assign_user_to_connection_url = guacamole_url + assign_user_to_connection_path

    path = "/connectionPermissions/" + vnc_identifier
    params = [{"op": "add", "path": path, "value": "READ"}]
    params = json.dumps(params)

    headers = {"Content-Type": "application/json", "Guacamole-Token": auth_token}

    response = requests.patch(
        assign_user_to_connection_url, data=params, headers=headers
    )
    return response.status_code


def get_http_login_format(identifier):
    response_generate_auth_token = generate_auth_token()
    auth_token = response_generate_auth_token["authToken"]
    guacamole_database = response_generate_auth_token["dataSource"]
    get_parameters_path = (
        "/api/session/data/"
        + guacamole_database
        + "/connections/"
        + identifier
        + "/parameters"
    )
    get_parameters_url = guacamole_url + get_parameters_path

    headers = {"Guacamole-Token": auth_token}

    parameters_res = requests.get(get_parameters_url, headers=headers)
    parameters_data = parameters_res.json()
    http_login_format = parameters_data["httpLoginFormat"]
    return http_login_format
