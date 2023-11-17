import Fastify from 'fastify';
import view from '@fastify/view';
import ejs from 'ejs';
import fastifyPostgres from '@fastify/postgres';
import formBodyPlugin from "@fastify/formbody";
import { routing } from './routing';

const main = async (): Promise<void> => {
  const fastify = Fastify({
    logger: true
  });

  fastify.register(view, {
    engine: {
      ejs:ejs
    }
  });

  fastify.register(fastifyPostgres, {
    connectionString: 'postgres://postgres@localhost/container'
  });

  fastify.register(formBodyPlugin);

  // Run the server!
  fastify.listen({ port: 3003, host: '0.0.0.0' }, (err: any, address: any) => {
    if (err) throw err;
    // Server is now listening on ${address}
  });

  await routing(fastify);
};

main();