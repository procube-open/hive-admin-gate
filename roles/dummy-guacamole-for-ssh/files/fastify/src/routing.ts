import { executor } from './executor';
import { sshType } from './vars';

export const routing = async (fastify: any) => {

  fastify.get('/', async (request: any, reply: any) => {
    const pg_client: any = await fastify.pg.connect();
    const work_sshs_query: any = await pg_client.query(
      'SELECT * FROM works order by work_id'
    );
    const wait_sshs_query: any = await pg_client.query(
      'SELECT * FROM waits order by work_id'
    );
    pg_client.release();
    const work_sshs_list: sshType[] = work_sshs_query.rows;
    const wait_sshs_list: sshType[] = wait_sshs_query.rows;
    return reply.view('/views/index.ejs', {work_sshs: work_sshs_list, wait_sshs: wait_sshs_list});

  });

  await fastify.post('/create', async (request: any, reply: any) => {
    const redirect_url: string = await executor('/create', request, fastify);
    reply.redirect(redirect_url);
  });

  await fastify.post('/connect', async (request: any, reply: any) => {
    const ssh_url: string = await executor('/connect', request, fastify);
    reply.redirect(ssh_url);
  });

  await fastify.post('/delete', async (request: any, reply: any) => {
    const redirect_url: string = await executor('/delete', request, fastify);
    reply.redirect(redirect_url);
  });

}



