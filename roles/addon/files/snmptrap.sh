#!/bin/bash

dest="10.33.198.66"
community="k0ptr0"
now=date

#zabbix parameter
to=$1
subject=$2
body=$3

declare -A selectOID=(
["Problem: Service weebgate restarted"]="1.3.6.1.4.1.35304.42.1.1"
["Problem: Service idm restarted"]="1.3.6.1.4.1.35304.42.2.1"
["Problem: Service ldap restarted"]="1.3.6.1.4.1.35304.42.3.1"
["Problem: Service am restarted"]="1.3.6.1.4.1.35304.42.4.1"
["Problem: Service amdb restarted"]="1.3.6.1.4.1.35304.42.5.1"
["Problem: Service guacamole restarted"]="1.3.6.1.4.1.35304.42.6.1"
["Problem: Service guacd restarted"]="1.3.6.1.4.1.35304.42.7.1"
["Problem: Service postgres restarted"]="1.3.6.1.4.1.35304.42.8.1"
["Problem: Service file-server restarted"]="1.3.6.1.4.1.35304.42.9.1"
["Problem: Service ftp-server restarted"]="1.3.6.1.4.1.35304.42.10.1"
["Problem: Service sftpserver restarted"]="1.3.6.1.4.1.35304.42.11.1"
["Problem: Service mongo restarted"]="1.3.6.1.4.1.35304.42.12.1"
["Problem: Service webdav-serveer restarted"]="1.3.6.1.4.1.35304.42.13.1"
["Problem: Service session-manager restarted"]="1.3.6.1.4.1.35304.42.14.1"
["Problem: Service weebgate replicas running percetage less than 100"]="1.3.6.1.4.1.35304.42.1.2"
["Problem: Service idm replicas running percetage less than 100"]="1.3.6.1.4.1.35304.42.2.2"
["Problem: Service ldap replicas running percetage less than 100"]="1.3.6.1.4.1.35304.42.3.2"
["Problem: Service am replicas running percetage less than 100"]="1.3.6.1.4.1.35304.42.4.2"
["Problem: Service amdb replicas running percetage less than 100"]="1.3.6.1.4.1.35304.42.5.2"            
["Problem: Service guacamole replicas running percetage less than 100"]="1.3.6.1.4.1.35304.42.6.2"       
["Problem: Service guacd replicas running percetage less than 100"]="1.3.6.1.4.1.35304.42.7.2"           
["Problem: Service postgres replicas running percetage less than 100"]="1.3.6.1.4.1.35304.42.8.2"        
["Problem: Service file-server replicas running percetage less than 100"]="1.3.6.1.4.1.35304.42.9.2"     
["Problem: Service ftp-server replicas running percetage less than 100"]="1.3.6.1.4.1.35304.42.10.2"     
["Problem: Service sftpserver replicas running percetage less than 100"]="1.3.6.1.4.1.35304.42.11.2"     
["Problem: Service mongo replicas running percetage less than 100"]="1.3.6.1.4.1.35304.42.12.2"          
["Problem: Service webdav-serveer replicas running percetage less than 100"]="1.3.6.1.4.1.35304.42.13.2" 
["Problem: Service session-manager replicas running percetage less than 100"]="1.3.6.1.4.1.35304.42.14.2"
["Problem: Exceed 90% Docker volume idm_mysql in idm usage"]="1.3.6.1.4.1.35304.42.2.3"
["Problem: Exceed 90% Docker volume idm_mongo in idm usage"]="1.3.6.1.4.1.35304.41.2.4"
["Problem: Exceed 90% Docker volume ldap_data in ldap usage"]="1.3.6.1.4.1.35304.42.3.3"
["Problem: Exceed 90% Docker volume amdb_data in amdb usage"]="1.3.6.1.4.1.35304.42.5.3"
["Problem: Exceed 90% Docker volume guacamole-recordings in guacd usage"]="1.3.6.1.4.1.35304.42.7.3"
["Problem: Exceed 90% Docker volume guacamole-db in postgres usage"]="1.3.6.1.4.1.35304.42.8.3"
["Problem: Exceed 90% Docker volume mongo-db in mongo usage"]="1.3.6.1.4.1.35304.42.12.3"
)

if [ "$subject" != "" ]; then
if [ -n "${selectOID["$subject"]}" ]; then
snmptrap -v 2c -c "$community" "$dest" '' "${selectOID["$subject"]}"
else
mkdir /tmp/log
file=$(mktemp /tmp/log/zabbix_traps.log_XXXXXX)
str="${now} '${subject}' was ignored instead of sent snmptrap."
echo "$str" >> "$file"
fi
fi
