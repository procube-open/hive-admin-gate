import axios from 'axios';
import { RequestBody } from './vars';

const session_manager = axios.create({
  baseURL: 'http://session-manager',
  headers: {
    'Content-Type': 'application/json'
  },
  responseType: 'json'
});

const guacamole = axios.create({
  baseURL: 'http://guacamole:8080/guacamole',
  responseType: 'json'
});

// コンテナを起動・停止するために、session-managerのapiに接続する
const access_session_manager = async (request_path: string, request_body: RequestBody): Promise<any> => {
  const get_session_manager_path = (request_path: string): string => {
    if (request_path == '/delete') {
      return '/delete';
    } else {
      return '/create';
    }
  }
  const session_manager_access_path: string = get_session_manager_path(request_path);
  const response_session_manager: any = await session_manager.post(session_manager_access_path, request_body);
  // const work_container: string = response_session_manager.data.work_container;
  return response_session_manager;
}

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
const create_vnc_connection = async (result_generate_token: any, create_vnc_connection_object: any): Promise<string> => {
  guacamole.defaults.headers.post['Content-Type'] = 'application/json';
  const guacamole_token: string = result_generate_token.data.authToken;
  const guacamole_database: string = result_generate_token.data.dataSource;
  const create_vnc_connection_path: string = '/api/session/data/' + guacamole_database + '/connections?token=' + guacamole_token;
  const result_create_vnc_connection: any = await guacamole.post(create_vnc_connection_path, create_vnc_connection_object);
  const vnc_identifier: string = result_create_vnc_connection.data.identifier;
  return vnc_identifier;
}

// guacamoleのapiに接続して、「接続」オブジェクトを削除する
const delete_vnc_connection = async (result_generate_token: any, request_body: RequestBody): Promise<void> => {
  guacamole.defaults.headers.post['Content-Type'] = 'application/json';
  const connection_id: any = request_body.connection_id;
  const guacamole_token: string = result_generate_token.data.authToken;
  const guacamole_database: string = result_generate_token.data.dataSource;
  const delete_vnc_connection_path: string = '/api/session/data/' + guacamole_database + '/connections/' + connection_id + '?token=' + guacamole_token;
  await guacamole.delete(delete_vnc_connection_path);
}

// guacamoleの「接続」オブジェクトを作成した時に得られた情報から、VNCに接続するためのURLを作成し、そのURLにリダイレクトする
const create_vnc_url = (vnc_identifier: string, guacamole_database: string): string => {
  const vnc_path: string = vnc_identifier + '\0c\0' + guacamole_database;
  const encoded_vnc_path: string = btoa(vnc_path);
  const vnc_url: string = '/guacamole/#/client/' + encoded_vnc_path;
  return vnc_url;
}

// データベース
const database_process_in_create = async (fastify: any, request_body: RequestBody, vnc_identifier: string, vnc_url: string, work_container: string): Promise<void> => {
  const wait_container_id: string = request_body.id;
  const work_id: string = request_body.work_id;

  const pg_client: any = await fastify.pg.connect();
  await pg_client.query(
    'DELETE FROM waits WHERE id=$1', [wait_container_id]
  );
  await pg_client.query(
    'INSERT INTO works (work_id, work_container, connection_id, vnc_url) VALUES ($1, $2, $3, $4)', [work_id, work_container, vnc_identifier, vnc_url]
  );
  pg_client.release();
}
const database_process_in_delete = async (fastify: any, request_body: RequestBody): Promise<void> => {
  const work_container_id: string = request_body.id;
  const work_id: string = request_body.work_id;
  const work_container: string = 'chrome-' + work_id;

  const pg_client: any = await fastify.pg.connect();
  await pg_client.query(
    'DELETE FROM works WHERE id=$1', [work_container_id]
  );
  await pg_client.query(
    'INSERT INTO waits (work_id, work_container) VALUES ($1, $2)', [work_id, work_container]
  );
  pg_client.release();
}

export const executor = async (request_path: string, request: any, fastify: any): Promise<string> => {

  // const vnc_password: string = 'secret';
  // const vnc_port: string = '5900';
  const request_body: RequestBody = request.body;
  // const work_id: string = request_body.work_id;
  // const username: string = request_body.username;
  // const password: string = request_body.password;
  const result_access_session_manager: any = await access_session_manager(request_path, request_body);

  // const create_vnc_connection_object: any = {
  //   "name": work_container,
  //   "parentIdentifier":"ROOT",
  //   "protocol":"vnc",
  //   "parameters":{
  //     "hostname": work_container,
  //     "port": vnc_port,
  //     "password": vnc_password
  //   },
  //   "attributes":{
  //     "guacd-encryption":null,
  //     "failover-only":null,
  //     "weight":null,
  //     "max-connections":"10",
  //     "guacd-hostname":null,
  //     "guacd-port":null,
  //     "max-connections-per-user":"10"
  //   }
  // };

  // const result_generate_token: any = await generate_auth_token(username, password);
  // const guacamole_database: string = result_generate_token.data.dataSource;

  const create_process = async (): Promise<string> => {
    // const vnc_identifier: string = await create_vnc_connection(result_generate_token, create_vnc_connection_object);
    const vnc_identifier: any = result_access_session_manager.data.vnc_identifier;
    const work_container: any = result_access_session_manager.data.work_container;
    const guacamole_database: string = 'postgresql';
    const vnc_url: string = create_vnc_url(vnc_identifier, guacamole_database);
    await database_process_in_create(fastify, request_body, vnc_identifier, vnc_url, work_container);
    return vnc_url;
  }

  const delete_process = async (): Promise<void> => {
    // await delete_vnc_connection(result_generate_token, request_body);
    await database_process_in_delete(fastify, request_body);
  }

  switch (request_path) {
    case '/create':
      await create_process();
      break;
    case '/connect':
      const vnc_url: string = await create_process();
      return vnc_url;
    case '/delete':
      await delete_process();
      break;
    default:
      break;
  }

  return '/dummy-guacamole-for-vnc/';

}



