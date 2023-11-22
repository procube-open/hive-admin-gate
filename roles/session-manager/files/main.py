from flask import Flask, request
import docker
import json
import os

app = Flask(__name__)
# image_chrome = 'procube/node-chrome'
image_chrome = os.environ.get('IMAGE_CHROME')
swarm_network = ['hive_default_network']

# コンテナが起動しない場合、以下の行（client = docker.from_env()）をコメントアウトしてデバッグしてみてください
client = docker.from_env()

@app.route('/create', methods=['POST'])
def service_create():
    work_container = 'chrome-' + request.json['work_id']
    selenium_allow_url = 'RULES=' + request.json['selenium_allow_url']
    backlog_username = 'USERNAME=' + request.json['backlog_username']
    backlog_password = 'PASSWORD=' + request.json['backlog_password']
    selenium_env = [selenium_allow_url, backlog_username, backlog_password]

    client.services.create(image_chrome, name=work_container, networks=swarm_network, env=selenium_env)
    return 'Successfully Created'

@app.route('/delete', methods=['POST'])
def service_delete():
    work_container = 'chrome-' + request.json['work_id']
    client.services.get(work_container).remove()
    return 'Successfully Dedeted'

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port='80')