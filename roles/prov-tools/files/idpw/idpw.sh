#!/bin/bash

HOSTNAME="dk0000-idpwmng91.eo.k-opti.ad.jp"
USER="idmanager"
CSV_DIR="/home/idmanager"
SCRIPT_DIR="/usr/local/bin"
RESULT="SUCCESS"

/root/prov/bin/python /root/idpw/generate_collaboration_csv.py

scp -i ~/.ssh/id_rsa /root/idpw/user_group.csv $USER@$HOSTNAME:$CSV_DIR
scp -i ~/.ssh/id_rsa /root/idpw/address_list.csv $USER@$HOSTNAME:$CSV_DIR
scp -i ~/.ssh/id_rsa /root/idpw/notification.csv $USER@$HOSTNAME:$CSV_DIR
scp -i ~/.ssh/id_rsa /root/idpw/user.csv $USER@$HOSTNAME:$CSV_DIR
scp -i ~/.ssh/id_rsa /root/idpw/user_admin.csv $USER@$HOSTNAME:$CSV_DIR

#ssh $USER@$HOSTNAME <<EOC
#$SCRIPT_DIR/idmng_coop_groups $CSV_DIR/user_group.csv
#$SCRIPT_DIR/idmng_coop_connections $CSV_DIR/address_list.csv
#$SCRIPT_DIR/idmng_coop_mails $CSV_DIR/notification.csv
#$SCRIPT_DIR/idmng_coop_users $CSV_DIR/user.csv
#$SCRIPT_DIR/idmng_coop_managers $CSV_DIR/user_admin.csv
#EOC

result1=`ssh $USER@$HOSTNAME $SCRIPT_DIR/idmng_coop_groups $CSV_DIR/user_group.csv`
total_result="SUCCESS"

if [ "$result1" = $RESULT ]; then
  echo "1:OK"

  result2=`ssh $USER@$HOSTNAME $SCRIPT_DIR/idmng_coop_connections $CSV_DIR/address_list.csv`

  if [ "$result2" = $RESULT ]; then
    echo "2:OK"
  else
    total_result="ERROR"
    echo "2:Fail"
    echo $result2
  fi

  result3=`ssh $USER@$HOSTNAME $SCRIPT_DIR/idmng_coop_mails $CSV_DIR/notification.csv`
  if [ "$result3" = $RESULT ]; then
    echo "3:OK"
  else
    total_result="ERROR"
    echo "3:Fail"
    echo $result3
  fi

  result4=`ssh $USER@$HOSTNAME $SCRIPT_DIR/idmng_coop_users $CSV_DIR/user.csv`
  if [ "$result4" = $RESULT ]; then
    echo "4:OK"

    result5=`ssh $USER@$HOSTNAME $SCRIPT_DIR/idmng_coop_managers $CSV_DIR/user_admin.csv`
    if [ "$result5" = $RESULT ]; then
      echo "5:OK"
    else
      total_result="ERROR"
      echo "5:Fail"
     echo $result5
    fi

  else
    total_result="ERROR"
    echo "4:Fail"
    echo $result4
  fi

else
  total_result="ERROR"
  echo "1:Fail"
  echo $result1
fi

echo $total_result
