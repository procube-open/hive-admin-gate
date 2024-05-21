#!/bin/bash

HOSTNAME=""
USER=""
CSV_DIR=""
SCRIPT_DIR=""

/root/prov/bin/python /root/idpw/generate_collaboration_csv.py

scp /root/idpw/user_group.csv $user@$hostname:$CSV_DIR
scp /root/idpw/address_list.csv $user@$hostname:$CSV_DIR
scp /root/idpw/notification.csv $user@$hostname:$CSV_DIR
scp /root/idpw/user.csv $user@$hostname:$CSV_DIR
scp /root/idpw/user_admin.csv $user@$hostname:$CSV_DIR

ssh $user@$hostname <<EOC
$SCRIPT_DIR/idmng_coop_groups $CSV_DIR/user_group.csv
$SCRIPT_DIR/idmng_coop_connections $CSV_DIR/address_list.csv
$SCRIPT_DIR/idmng_coop_mails $CSV_DIR/notification.csv
$SCRIPT_DIR/idmng_coop_users $CSV_DIR/user.csv
$SCRIPT_DIR/idmng_coop_managers $CSV_DIR/user_admin.csv
EOC
done
