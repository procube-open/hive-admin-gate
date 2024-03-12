#! /bin/sh

/usr/sbin/crond
exec /sbin/tini -- python /root/session-manager/main.py
