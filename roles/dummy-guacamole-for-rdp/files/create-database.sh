#! /bin/sh

su postgres -c 'initdb -D /var/lib/postgresql/data'
su postgres -c 'pg_ctl start -D /var/lib/postgresql/data'
su postgres -c 'createdb rdp'
psql -d rdp -U postgres -c 'CREATE TABLE works(id serial PRIMARY KEY, work_id VARCHAR (8) NOT NULL, work_rdp VARCHAR (16) NOT NULL, connection_id VARCHAR (8) NOT NULL, rdp_url VARCHAR (255) NOT NULL);'
psql -d rdp -U postgres -c 'CREATE TABLE waits(id serial PRIMARY KEY, work_id VARCHAR (8) NOT NULL, work_rdp VARCHAR (16) NOT NULL);'

for i in `seq 0 100`
do
  echo "INSERT INTO waits (work_id, work_rdp) VALUES ('AA$i', 'windows-AA$i');" >> /var/tmp/rdp.sql
done

psql -d rdp -U postgres -f /var/tmp/rdp.sql





# psql -d rdp -U postgres -c "INSERT INTO waits (work_id, work_rdp) VALUES ('AA001', 'windows-AA001');"
# psql -d rdp -U postgres -c "INSERT INTO waits (work_id, work_rdp) VALUES ('BB001', 'windows-BB001');"
# psql -d rdp -U postgres -c "INSERT INTO waits (work_id, work_rdp) VALUES ('CC001', 'windows-CC001');"
# psql -d rdp -U postgres -c "INSERT INTO waits (work_id, work_rdp) VALUES ('DD001', 'windows-DD001');"
# psql -d rdp -U postgres -c "INSERT INTO waits (work_id, work_rdp) VALUES ('EE001', 'windows-EE001');"
# psql -d rdp -U postgres -c "INSERT INTO waits (work_id, work_rdp) VALUES ('FF001', 'windows-FF001');"
# psql -d rdp -U postgres -c "INSERT INTO waits (work_id, work_rdp) VALUES ('GG001', 'windows-GG001');"
