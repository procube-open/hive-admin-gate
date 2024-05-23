#!/bin/bash

HOSTNAME="dk0000-idpwmng91.eo.k-opti.ad.jp"
USER="idmanager"
CSV_DIR="/home/idmanager"
SCRIPT_DIR="/usr/local/bin"

/root/prov/bin/python /root/idpw/generate_collaboration_csv.py
 
scp -i .ssh/id_rsa /root/idpw/user_group.csv $USER@$HOSTNAME:$CSV_DIR
scp -i .ssh/id_rsa /root/idpw/address_list.csv $USER@$HOSTNAME:$CSV_DIR
scp -i .ssh/id_rsa /root/idpw/notification.csv $USER@$HOSTNAME:$CSV_DIR
scp -i .ssh/id_rsa /root/idpw/user.csv $USER@$HOSTNAME:$CSV_DIR
scp -i .ssh/id_rsa /root/idpw/user_admin.csv $USER@$HOSTNAME:$CSV_DIR

ssh $user@$hostname <<EOC
$SCRIPT_DIR/idmng_coop_groups $CSV_DIR/user_group.csv
$SCRIPT_DIR/idmng_coop_connections $CSV_DIR/address_list.csv
$SCRIPT_DIR/idmng_coop_mails $CSV_DIR/notification.csv
$SCRIPT_DIR/idmng_coop_users $CSV_DIR/user.csv
$SCRIPT_DIR/idmng_coop_managers $CSV_DIR/user_admin.csv
EOC
done
