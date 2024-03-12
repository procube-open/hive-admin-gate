#! /bin/sh

su postgres -c 'initdb -D /var/lib/postgresql/data'
su postgres -c 'pg_ctl start -D /var/lib/postgresql/data'
su postgres -c 'createdb ssh'
psql -d ssh -U postgres -c 'CREATE TABLE works(id serial PRIMARY KEY, work_id VARCHAR (8) NOT NULL, work_ssh VARCHAR (16) NOT NULL, connection_id VARCHAR (8) NOT NULL, ssh_url VARCHAR (255) NOT NULL);'
psql -d ssh -U postgres -c 'CREATE TABLE waits(id serial PRIMARY KEY, work_id VARCHAR (8) NOT NULL, work_ssh VARCHAR (16) NOT NULL);'

for i in `seq 0 100`
do
  echo "INSERT INTO waits (work_id, work_ssh) VALUES ('AA$i', 'ssh-AA$i');" >> /var/tmp/ssh.sql
done

psql -d ssh -U postgres -f /var/tmp/ssh.sql


# psql -d ssh -U postgres -c "INSERT INTO waits (work_id, work_ssh) VALUES ('AA001', 'ssh-AA001');"
# psql -d ssh -U postgres -c "INSERT INTO waits (work_id, work_ssh) VALUES ('BB001', 'ssh-BB001');"
# psql -d ssh -U postgres -c "INSERT INTO waits (work_id, work_ssh) VALUES ('CC001', 'ssh-CC001');"
# psql -d ssh -U postgres -c "INSERT INTO waits (work_id, work_ssh) VALUES ('DD001', 'ssh-DD001');"
# psql -d ssh -U postgres -c "INSERT INTO waits (work_id, work_ssh) VALUES ('EE001', 'ssh-EE001');"
# psql -d ssh -U postgres -c "INSERT INTO waits (work_id, work_ssh) VALUES ('FF001', 'ssh-FF001');"
# psql -d ssh -U postgres -c "INSERT INTO waits (work_id, work_ssh) VALUES ('GG001', 'ssh-GG001');"

