#!/bin/bash

dest="172.21.35.129"
community=“public”
now=date

#zabbix parameter
to=$1
subject=$2
body=$3

declare -A selectOID=(
["Problem: Service log-recorder restarted"]="1.3.6.1.4.1.35304.41.1.1"
["Problem: Service log-recorder-web restarted"]="1.3.6.1.4.1.35304.41.2.1"
["Problem: Service log-recorder replicas running percetage less than 100"]="1.3.6.1.4.1.35304.41.1.2"
["Problem: Service log-recorder-web replicas running percetage less than 100"]="1.3.6.1.4.1.35304.41.2.2"
["Problem: Exceed 90% Docker volume logdb_data in nslrdb usage"]="1.3.6.1.4.1.35304.41.3.1"
["Problem: Exceed 90% Docker volume syslog_data in nslrdb usage"]="1.3.6.1.4.1.35304.41.4.1"
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
