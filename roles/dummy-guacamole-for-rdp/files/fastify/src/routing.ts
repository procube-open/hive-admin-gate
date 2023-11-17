import { executor } from './executor';
import { rdpType } from './vars';

export const routing = async (fastify: any) => {

  fastify.get('/', async (request: any, reply: any) => {
    const pg_client: any = await fastify.pg.connect();
    const work_rdps_query: any = await pg_client.query(
      'SELECT * FROM works order by work_id'
    );
    const wait_rdps_query: any = await pg_client.query(
      'SELECT * FROM waits order by work_id'
    );
    pg_client.release();
    const work_rdps_list: rdpType[] = work_rdps_query.rows;
    const wait_rdps_list: rdpType[] = wait_rdps_query.rows;
    return reply.view('/views/index.ejs', {work_rdps: work_rdps_list, wait_rdps: wait_rdps_list});

  });

  await fastify.post('/create', async (request: any, reply: any) => {
    const redirect_url: string = await executor('/create', request, fastify);
    reply.redirect(redirect_url);
  });

  await fastify.post('/connect', async (request: any, reply: any) => {
    const rdp_url: string = await executor('/connect', request, fastify);
    reply.redirect(rdp_url);
  });

  await fastify.post('/delete', async (request: any, reply: any) => {
    const redirect_url: string = await executor('/delete', request, fastify);
    reply.redirect(redirect_url);
  });

}



