[1mdiff --git a/roles/idm/tasks/main.yml b/roles/idm/tasks/main.yml[m
[1mindex 48d1d3f..e7c3f44 100644[m
[1m--- a/roles/idm/tasks/main.yml[m
[1m+++ b/roles/idm/tasks/main.yml[m
[36m@@ -104,42 +104,3 @@[m
 #     path: /usr/local/NetSoarer/IDManager/BindBroker/config/default.js[m
 #     regexp: "debug :"[m
 #     line: "             debug : false,"[m
[31m-- name: copy AD cert file[m
[31m-  copy:[m
[31m-    src: "{{ item.src }}"[m
[31m-    dest: "{{ item.dest }}"[m
[31m-  loop:[m
[31m-  - src: tca-AEZB00-TCADC12-CA.cer[m
[31m-    dest: /tmp/tca-AEZB00-TCADC12-CA.cer[m
[31m-  - src: tws-AEZB00-TWSDC12-CA.cer[m
[31m-    dest: /tmp/tws-AEZB00-TWSDC12-CA.cer[m
[31m-- name: Add entry to /etc/hosts file[m
[31m-  lineinfile:[m
[31m-    path: /etc/hosts[m
[31m-    line: "{{ item.ip }} {{ item.name }}"[m
[31m-    state: present[m
[31m-  loop:[m
[31m-  - ip: 10.35.107.25[m
[31m-    name: AEZB00-TCADC11.tca.eo.k-opti.ad.jp[m
[31m-  - ip: 10.35.107.26[m
[31m-    name: AEZB00-TCADC12.tca.eo.k-opti.ad.jp[m
[31m-  - ip: 10.35.47.25[m
[31m-    name: DK0000-TCADC11.tca.eo.k-opti.ad.jp[m
[31m-  - ip: 10.35.107.27[m
[31m-    name: AEZB00-TWSDC11.tws.eo.k-opti.ad.jp[m
[31m-  - ip: 10.35.107.28[m
[31m-    name: AEZB00-TWSDC12.tws.eo.k-opti.ad.jp[m
[31m-  - ip: 10.35.47.27[m
[31m-    name: DK0000-TWSDC11.tws.eo.k-opti.ad.jp[m
[31m-- name: Import certificate[m
[31m-  community.general.java_cert:[m
[31m-    cert_path: "{{ item.path }}"[m
[31m-    cert_alias: "{{ item.name }}"[m
[31m-    keystore_path: /usr/lib/jvm/adoptopenjdk-11-hotspot/lib/security/cacerts[m
[31m-    keystore_pass: changeit[m
[31m-    keystore_create: true[m
[31m-  loop:[m
[31m-  - path: /tmp/tca-AEZB00-TCADC12-CA.cer[m
[31m-    name: tcaCert[m
[31m-  - path: /tmp/tws-AEZB00-TWSDC12-CA.cer[m
[31m-    name: twsCert[m
