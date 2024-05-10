import docker
import os
import requests
import datetime
from access_guacamole import generate_auth_token
from insert_hosts import insert_hosts

print("Started cleaning davfs volumes")

guacamole_url = os.environ.get("GUACAMOLE_URL")
response_generate_auth_token = generate_auth_token()
auth_token = response_generate_auth_token["authToken"]
guacamole_database = response_generate_auth_token["dataSource"]
get_works_path = (
    "/api/session/data/" + guacamole_database + "/works?token=" + auth_token
)
get_works_url = guacamole_url + get_works_path
works_res = requests.get(get_works_url)
works_data = works_res.json()
today = datetime.datetime.today()

tls_config = docker.tls.TLSConfig(
    ca_cert="/root/.docker/ca.pem",
    verify=True,
    client_cert=("/root/.docker/cert.pem", "/root/.docker/key.pem"),
)

base_urls = []
insert_hosts(base_urls)

for base_url in base_urls:
    client = docker.APIClient(base_url=base_url, tls=tls_config)
    filters = {"driver": "fentas/davfs:latest"}
    davfs_volumes = client.volumes(filters=filters)

    for davfs_volume in davfs_volumes["Volumes"]:
        try:
            davfs_volume_name = davfs_volume["Name"]
            davfs_volume_name_list = davfs_volume_name.split("-")
            davfs_volume_work_id = davfs_volume_name_list[2]

            if davfs_volume_work_id == "public":
                break

            for v in reversed(works_data.values()):
                if v["idmIdentifier"] == davfs_volume_work_id:
                    rm_flag: bool = True
                    for period in v["periods"]:
                        valid_until_date = datetime.datetime.strptime(
                            period["validUntil"], "%Y-%m-%d"
                        )
                        if valid_until_date > today:
                            rm_flag = False
                            break
                    if rm_flag:
                        client.remove_volume(davfs_volume_name, force=True)
                        logger_text = davfs_volume_name + " Deleted. HOST:" + base_url
                        print(logger_text)

                    break

        except Exception as e:
            print(e)
            continue

print("Ended cleaning davfs volumes")
