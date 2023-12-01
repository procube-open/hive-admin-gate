import axios from 'axios';
import { RequestBody, rdp_password } from './vars';

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
const create_rdp_connection = async (result_generate_token: any, create_rdp_connection_object: any): Promise<string> => {
  guacamole.defaults.headers.post['Content-Type'] = 'application/json';
  const guacamole_token: string = result_generate_token.data.authToken;
  const guacamole_database: string = result_generate_token.data.dataSource;
  const create_rdp_connection_path: string = '/api/session/data/' + guacamole_database + '/connections?token=' + guacamole_token;
  const result_create_rdp_connection: any = await guacamole.post(create_rdp_connection_path, create_rdp_connection_object);
  const rdp_identifier: string = result_create_rdp_connection.data.identifier;
  return rdp_identifier;
}

// guacamoleのapiに接続して、「接続」オブジェクトを削除する
const delete_rdp_connection = async (result_generate_token: any, request_body: RequestBody): Promise<void> => {
  guacamole.defaults.headers.post['Content-Type'] = 'application/json';
  const connection_id: any = request_body.connection_id;
  const guacamole_token: string = result_generate_token.data.authToken;
  const guacamole_database: string = result_generate_token.data.dataSource;
  const delete_rdp_connection_path: string = '/api/session/data/' + guacamole_database + '/connections/' + connection_id + '?token=' + guacamole_token;
  await guacamole.delete(delete_rdp_connection_path);
}

// guacamoleの「接続」オブジェクトを作成した時に得られた情報から、rdpに接続するためのURLを作成し、そのURLにリダイレクトする
const create_rdp_url = (rdp_identifier: string, guacamole_database: string): string => {
  const rdp_path: string = rdp_identifier + '\0c\0' + guacamole_database;
  const encoded_rdp_path: string = btoa(rdp_path);
  const rdp_url: string = '/guacamole/#/client/' + encoded_rdp_path;
  return rdp_url;
}

// データベース
const database_process_in_create = async (fastify: any, request_body: RequestBody, rdp_identifier: string, rdp_url: string): Promise<void> => {
  const wait_rdp_id: string = request_body.id;
  const work_id: string = request_body.work_id;
  const work_rdp: string = 'windows-' + work_id;

  const pg_client: any = await fastify.pg.connect();
  await pg_client.query(
    'DELETE FROM waits WHERE id=$1', [wait_rdp_id]
  );
  await pg_client.query(
    'INSERT INTO works (work_id, work_rdp, connection_id, rdp_url) VALUES ($1, $2, $3, $4)', [work_id, work_rdp, rdp_identifier, rdp_url]
  );
  pg_client.release();
}
const database_process_in_delete = async (fastify: any, request_body: RequestBody): Promise<void> => {
  const work_rdp_id: string = request_body.id;
  const work_id: string = request_body.work_id;
  const work_rdp: string = 'windows-' + work_id;

  const pg_client: any = await fastify.pg.connect();
  await pg_client.query(
    'DELETE FROM works WHERE id=$1', [work_rdp_id]
  );
  await pg_client.query(
    'INSERT INTO waits (work_id, work_rdp) VALUES ($1, $2)', [work_id, work_rdp]
  );
  pg_client.release();
}

export const executor = async (request_path: string, request: any, fastify: any): Promise<string> => {

  const rdp_username: string = 'nigauri';
  const rdp_port: string = '3389';
  const request_body: RequestBody = request.body;
  const work_id: string = request_body.work_id;
  const work_rdp: string = 'windows-' + work_id;
  const username: string = request_body.username;
  const password: string = request_body.password;

  const create_rdp_connection_object: any = {
    "name": work_rdp,
    "parentIdentifier":"ROOT",
    "protocol":"rdp",
    "parameters":{
      "hostname": "192.168.10.2",
      "port": rdp_port,
      "ignore-cert": "true",
      "username": rdp_username,
      "password": rdp_password
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
    const rdp_identifier: string = await create_rdp_connection(result_generate_token, create_rdp_connection_object);
    const rdp_url: string = create_rdp_url(rdp_identifier, guacamole_database);
    await database_process_in_create(fastify, request_body, rdp_identifier, rdp_url);
    return rdp_url;
  }

  const delete_process = async (): Promise<void> => {
    await delete_rdp_connection(result_generate_token, request_body);
    await database_process_in_delete(fastify, request_body);
  }

  switch (request_path) {
    case '/create':
      await create_process();
      break;
    case '/connect':
      const rdp_url: string = await create_process();
      return rdp_url;
    case '/delete':
      await delete_process();
      break;
    default:
      break;
  }

  return '/dummy-guacamole-for-rdp/';

}



