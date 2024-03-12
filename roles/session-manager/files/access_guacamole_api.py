import json
import os
import requests
import urllib

guacamole_url = os.environ.get('GUACAMOLE_URL')

def generate_auth_token():
    generate_auth_token_path = '/api/tokens'
    generate_auth_token_url = guacamole_url + generate_auth_token_path

    username = os.environ.get('GUACAMOLE_USERNAME')
    password = os.environ.get('GUACAMOLE_PASSWORD')
    params = {
        'username': username,
        'password': password
    }
    params = urllib.parse.urlencode(params)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(generate_auth_token_url, data=params, headers=headers)
    return response.json()

def create_vnc_connection(work_container):
    response_generate_auth_token = generate_auth_token()
    auth_token = response_generate_auth_token['authToken']
    guacamole_database = response_generate_auth_token['dataSource']
    create_vnc_connection_path = '/api/session/data/' + guacamole_database + '/connections?token=' + auth_token
    create_vnc_connection_url = guacamole_url + create_vnc_connection_path

    vnc_port = os.environ.get('VNC_PORT')
    vnc_password = os.environ.get('VNC_PASSWORD')
    params = {
        "name": work_container,
        "parentIdentifier":"ROOT",
        "protocol":"vnc",
        "parameters":{
            "hostname": work_container,
            "port": vnc_port,
            "password": vnc_password
        },
        "attributes":{
            "guacd-encryption": "",
            "failover-only": "",
            "weight": "",
            "max-connections":"10",
            "guacd-hostname": "",
            "guacd-port": "",
            "max-connections-per-user":"10"
        }
    }
    params = json.dumps(params)

    headers = {'Content-Type': 'application/json'}

    response = requests.post(create_vnc_connection_url, data=params, headers=headers)
    return response.json()

def delete_vnc_connection(vnc_identifier):
    response_generate_auth_token = generate_auth_token()
    auth_token = response_generate_auth_token['authToken']
    guacamole_database = response_generate_auth_token['dataSource']
    delete_vnc_connection_path = '/api/session/data/' + guacamole_database + '/connections/' + vnc_identifier + '?token=' + auth_token
    delete_vnc_connection_url = guacamole_url + delete_vnc_connection_path

    headers = {'Content-Type': 'application/json'}

    response = requests.delete(delete_vnc_connection_url, headers=headers)
