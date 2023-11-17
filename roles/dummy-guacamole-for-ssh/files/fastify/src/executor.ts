import axios from 'axios';
import { RequestBody, ssh_private_key, ssh_username, ssh_hostname } from './vars';

const guacamole = axios.create({
  baseURL: 'http://guacamole:8080/guacamole',
  responseType: 'json'
});

// guacamoleのapiに接続して、authTokenを取得する
const generate_auth_token = async (username: string, password: string): Promise<any> => {
  guacamole.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  const generate_token_path: string = '/api/tokens';
  const generate_token_params = new URLSearchParams();
  generate_token_params.append('username', username);
  generate_token_params.append('password', password);
  const result_generate_token: any = await guacamole.post(generate_token_path, generate_token_params);
  return result_generate_token;
}

// guacamoleのapiに接続して、「接続」オブジェクトを作成する
const create_ssh_connection = async (result_generate_token: any, create_ssh_connection_object: any): Promise<string> => {
  guacamole.defaults.headers.post['Content-Type'] = 'application/json';
  const guacamole_token: string = result_generate_token.data.authToken;
  const guacamole_database: string = result_generate_token.data.dataSource;
  const create_ssh_connection_path: string = '/api/session/data/' + guacamole_database + '/connections?token=' + guacamole_token;
  const result_create_ssh_connection: any = await guacamole.post(create_ssh_connection_path, create_ssh_connection_object);
  const ssh_identifier: string = result_create_ssh_connection.data.identifier;
  return ssh_identifier;
}

// guacamoleのapiに接続して、「接続」オブジェクトを削除する
const delete_ssh_connection = async (result_generate_token: any, request_body: RequestBody): Promise<void> => {
  guacamole.defaults.headers.post['Content-Type'] = 'application/json';
  const connection_id: any = request_body.connection_id;
  const guacamole_token: string = result_generate_token.data.authToken;
  const guacamole_database: string = result_generate_token.data.dataSource;
  const delete_ssh_connection_path: string = '/api/session/data/' + guacamole_database + '/connections/' + connection_id + '?token=' + guacamole_token;
  await guacamole.delete(delete_ssh_connection_path);
}

// guacamoleの「接続」オブジェクトを作成した時に得られた情報から、sshに接続するためのURLを作成し、そのURLにリダイレクトする
const create_ssh_url = (ssh_identifier: string, guacamole_database: string): string => {
  const ssh_path: string = ssh_identifier + '\0c\0' + guacamole_database;
  const encoded_ssh_path: string = btoa(ssh_path);
  const ssh_url: string = 'https://guacamole.admin-gate-simulation.procube-demo.jp/guacamole/#/client/' + encoded_ssh_path;
  // const ssh_url: string = 'https://localhost:19443/#/client/' + encoded_ssh_path;
  return ssh_url;
}

// データベース
const database_process_in_create = async (fastify: any, request_body: RequestBody, ssh_identifier: string, ssh_url: string): Promise<void> => {
  const wait_ssh_id: string = request_body.id;
  const work_id: string = request_body.work_id;
  const work_ssh: string = 'ssh-' + work_id;

  const pg_client: any = await fastify.pg.connect();
  await pg_client.query(
    'DELETE FROM waits WHERE id=$1', [wait_ssh_id]
  );
  await pg_client.query(
    'INSERT INTO works (work_id, work_ssh, connection_id, ssh_url) VALUES ($1, $2, $3, $4)', [work_id, work_ssh, ssh_identifier, ssh_url]
  );
  pg_client.release();
}
const database_process_in_delete = async (fastify: any, request_body: RequestBody): Promise<void> => {
  const work_ssh_id: string = request_body.id;
  const work_id: string = request_body.work_id;
  const work_ssh: string = 'ssh-' + work_id;

  const pg_client: any = await fastify.pg.connect();
  await pg_client.query(
    'DELETE FROM works WHERE id=$1', [work_ssh_id]
  );
  await pg_client.query(
    'INSERT INTO waits (work_id, work_ssh) VALUES ($1, $2)', [work_id, work_ssh]
  );
  pg_client.release();
}

export const executor = async (request_path: string, request: any, fastify: any): Promise<string> => {

  const ssh_port: string = '22';
  const request_body: RequestBody = request.body;
  const work_id: string = request_body.work_id;
  const work_ssh: string = 'ssh-' + work_id;
  const username: string = request_body.username;
  const password: string = request_body.password;

  const create_ssh_connection_object: any = {
    "name": work_ssh,
    "parentIdentifier":"ROOT",
    "protocol":"ssh",
    "parameters":{
      "hostname": ssh_hostname,
      "port": ssh_port,
      "username": ssh_username,
      "private-key": ssh_private_key
    },
    "attributes":{
      "guacd-encryption":null,
      "failover-only":null,
      "weight":null,
      "max-connections":"10",
      "guacd-hostname":null,
      "guacd-port":null,
      "max-connections-per-user":"10"
    }
  };

  const result_generate_token: any = await generate_auth_token(username, password);
  const guacamole_database: string = result_generate_token.data.dataSource;

  const create_process = async (): Promise<string> => {
    const ssh_identifier: string = await create_ssh_connection(result_generate_token, create_ssh_connection_object);
    const ssh_url: string = create_ssh_url(ssh_identifier, guacamole_database);
    await database_process_in_create(fastify, request_body, ssh_identifier, ssh_url);
    return ssh_url;
  }

  const delete_process = async (): Promise<void> => {
    await delete_ssh_connection(result_generate_token, request_body);
    await database_process_in_delete(fastify, request_body);
  }

  switch (request_path) {
    case '/create':
      await create_process();
      break;
    case '/connect':
      // sshコンテナが起動してからリダイレクトされるように、3.5秒待つようにする
      const get_ssh_url = async (): Promise<string> => {
        return new Promise( async (resolve) => {
          const ssh_url: string = await create_process();
          setTimeout(() => {
            resolve(ssh_url);
          }, 3500);
        });
      }
      const ssh_url: string = await get_ssh_url();
      return ssh_url;
    case '/delete':
      await delete_process();
      break;
    default:
      break;
  }

  return 'https://guacamole.admin-gate-simulation.procube-demo.jp/dummy-g3/';
  // return 'http://localhost:3004/';

}



