#! /bin/sh

su postgres -c 'initdb -D /var/lib/postgresql/data'
su postgres -c 'pg_ctl start -D /var/lib/postgresql/data'
su postgres -c 'createdb container'
psql -d container -U postgres -c 'CREATE TABLE works(id serial PRIMARY KEY, work_id VARCHAR (8) NOT NULL, work_container VARCHAR (255) NOT NULL, connection_id VARCHAR (8) NOT NULL, vnc_url VARCHAR (255) NOT NULL);'
psql -d container -U postgres -c 'CREATE TABLE waits(id serial PRIMARY KEY, work_id VARCHAR (8) NOT NULL, work_container VARCHAR (16) NOT NULL);'

for i in `seq -w 0 50`
do
  echo "INSERT INTO waits (work_id, work_container) VALUES ('AAA$i', 'chrome-AAA$i');" >> /var/tmp/container.sql
done

psql -d container -U postgres -f /var/tmp/container.sql

# psql -d container -U postgres -c "INSERT INTO waits (work_id, work_container) VALUES ('AA001', 'chrome-AA001');"
# psql -d container -U postgres -c "INSERT INTO waits (work_id, work_container) VALUES ('BB001', 'chrome-BB001');"
# psql -d container -U postgres -c "INSERT INTO waits (work_id, work_container) VALUES ('CC001', 'chrome-CC001');"
# psql -d container -U postgres -c "INSERT INTO waits (work_id, work_container) VALUES ('DD001', 'chrome-DD001');"
# psql -d container -U postgres -c "INSERT INTO waits (work_id, work_container) VALUES ('EE001', 'chrome-EE001');"
# psql -d container -U postgres -c "INSERT INTO waits (work_id, work_container) VALUES ('FF001', 'chrome-FF001');"
# psql -d container -U postgres -c "INSERT INTO waits (work_id, work_container) VALUES ('GG001', 'chrome-GG001');"