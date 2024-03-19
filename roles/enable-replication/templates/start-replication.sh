#! /bin/bash

# scpでlatestのバックアップファイルを/home/admin/backup配下に置く

for SERVICE in mongo idm
do
  hive-backup.sh -l $SERVICE -r
done