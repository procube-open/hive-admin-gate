import { executor } from './executor';
import { ContainerType } from './vars';

export const routing = async (fastify: any) => {

  fastify.get('/', async (request: any, reply: any) => {
    const pg_client: any = await fastify.pg.connect();
    const work_containers_query: any = await pg_client.query(
      'SELECT * FROM works order by work_id'
    );
    const wait_containers_query: any = await pg_client.query(
      'SELECT * FROM waits order by work_id'
    );
    pg_client.release();
    const work_containers_list: ContainerType[] = work_containers_query.rows;
    const wait_containers_list: ContainerType[] = wait_containers_query.rows;
    const selenium_allow_urls: string[] = ['procube.info', 'backlog.jp', 'google.com'];
    return reply.view('/views/index.ejs', {work_containers: work_containers_list, wait_containers: wait_containers_list, selenium_allow_urls: selenium_allow_urls});

  });

  await fastify.post('/create', async (request: any, reply: any) => {
    const redirect_url: string = await executor('/create', request, fastify);
    reply.redirect(redirect_url);
  });

  await fastify.post('/connect', async (request: any, reply: any) => {
    const vnc_url: string = await executor('/connect', request, fastify);
    reply.redirect(vnc_url);
  });

  await fastify.post('/delete', async (request: any, reply: any) => {
    const redirect_url: string = await executor('/delete', request, fastify);
    reply.redirect(redirect_url);
  });

}



