import json
import os
import requests
from access_guacamole_api import generate_auth_token

print("Started cleaning chrome containers")

guacamole_url = os.environ.get("GUACAMOLE_URL")
response_generate_auth_token = generate_auth_token()
auth_token = response_generate_auth_token["authToken"]
guacamole_database = response_generate_auth_token["dataSource"]
get_connections_path = (
    "/api/session/data/" + guacamole_database + "/connections?token=" + auth_token
)
get_connections_url = guacamole_url + get_connections_path
connections_res = requests.get(get_connections_url)
connections_data = connections_res.json()

for v in connections_data.values():
    try:
        if (
            v["idmIdentifier"] == "session-manager"
            and v["protocol"] == "vnc"
            and v["activeConnections"] == 0
        ):
            print("delete " + v["name"])
            delete_url = "http://localhost:80/delete"
            params = {"work_container": v["name"], "vnc_identifier": v["identifier"]}
            params = json.dumps(params)
            headers = {"Content-Type": "application/json"}
            requests.post(delete_url, data=params, headers=headers)
    except Exception as e:
        print(e)
        continue

print("Ended cleaning chrome containers")
