import json
import os
import requests
import urllib
import uuid

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


def get_user(token: str):
    get_user_path = "/api/tokens"
    get_user_url = guacamole_url + get_user_path

    params = {"token": token}
    params = urllib.parse.urlencode(params)

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(get_user_url, data=params, headers=headers)
    return response.json()


def create_connection(
    token: str,
    database: str,
    work_id: str,
    protocol: str,
    hostname: str,
    port: str,
    username: str | None,
    password: str | None,
    httpLoginFormat: str | None,
    originIdentifier: str | None,
):
    create_connection_path = (
        "/api/session/data/" + database + "/connections?token=" + token
    )
    create_connection_url = guacamole_url + create_connection_path

    params = json.dumps(
        {
            "name": hostname + ":" + str(uuid.uuid4()),
            "parentIdentifier": "ROOT",
            "protocol": protocol,
            "idmIdentifier": "changepw" if work_id == "changepw" else "session-manager",
            "parameters": {
                "work_id": work_id,
                "hostname": hostname,
                "port": port,
                "username": username,
                "password": password,
                "httpLoginFormat": httpLoginFormat,
                "originIdentifier": originIdentifier,
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
    )
    headers = {"Content-Type": "application/json"}

    response = requests.post(create_connection_url, data=params, headers=headers)
    return response.json()


def delete_connection(token: str, database: str, identifier: str) -> None:
    delete_vnc_connection_path = (
        "/api/session/data/"
        + database
        + "/connections/"
        + identifier
        + "?token="
        + token
    )
    delete_vnc_connection_url = guacamole_url + delete_vnc_connection_path

    headers = {"Content-Type": "application/json"}

    requests.delete(delete_vnc_connection_url, headers=headers)
    return


def assign_user_to_connection(
    token: str, database: str, username: str, identifier: str
) -> None:
    assign_user_to_connection_path = (
        "/api/session/data/" + database + "/users/" + username + "/permissions"
    )
    assign_user_to_connection_url = guacamole_url + assign_user_to_connection_path

    path = "/connectionPermissions/" + identifier
    params = json.dumps([{"op": "add", "path": path, "value": "READ"}])

    headers = {"Content-Type": "application/json", "Guacamole-Token": token}

    requests.patch(assign_user_to_connection_url, data=params, headers=headers)
    return


def get_connection_info(token: str, database: str, identifier: str):
    get_parameters_path = "/api/session/data/" + database + "/connections/" + identifier
    get_parameters_url = guacamole_url + get_parameters_path

    headers = {"Guacamole-Token": token}

    parameters_res = requests.get(get_parameters_url, headers=headers)
    return parameters_res.json()


def get_connection_params(token: str, database: str, identifier: str):
    get_parameters_path = (
        "/api/session/data/" + database + "/connections/" + identifier + "/parameters"
    )
    get_parameters_url = guacamole_url + get_parameters_path

    headers = {"Guacamole-Token": token}

    parameters_res = requests.get(get_parameters_url, headers=headers)
    return parameters_res.json()


def get_work_from_identifier(token: str, database: str, idmIdentifier: str):
    get_works_path = "/api/session/data/" + database + "/works"
    get_works_url = guacamole_url + get_works_path
    headers = {"Guacamole-Token": token}
    works_res = requests.get(get_works_url,  headers=headers)
    works_data = works_res.json()
    for v in reversed(works_data.values()):
        if v["idmIdentifier"] == idmIdentifier:
            return v

    raise Exception("Work not found")
