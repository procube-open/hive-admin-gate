import csv
import requests

base_url = 'http://localhost:8090/IDManager'
user_url = base_url + '/userEditorInterface'
user_group_url = base_url + '/SystemUserGroupIF'
req_header = {'HTTP_SYSTEMACCOUNT': 'SYSTEM'}


def find_user_group(gid, user_group):
    rl = list(filter(lambda x: gid in user_group))
    return rl[0] if len(rl) > 0 else {'sAMAccountName':'', 'gidNumber':''}


if __name__=="__main__":
    user_req = requests.get(user_url, headers=req_header)
    user_group_req = requests.get(user_group_url, headers=req_header)
    user = user_req.json()
    user_group = user_group_req.json()

    with open('user_group.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for ug in user_group:
            row = [
                ug['ou'],
                ug['name'],
                ug['gid']
            ]
            writer.writerow(row)

    with open('address_list.csv', mode='w', encoding='uft-8', newline='') as file:
        writer = csv.writer(file)
        for ug in user_group:
            for ug_allow in ug['allowedAddressList']:
                row = [
                    ug['ou'],
                    '0',
                    ug_allow
                ]
                writer.writerow(row)
            for ug_forbidden in ug['forbiddenAddressList']:
                row = [
                    ug['ou'],
                    '1',
                    ug_forbidden
                ]
                writer.writerow(row)
    
    with open('notification.csv', mode='w', encoding='uft-8', newline='') as file:
        writer = csv.writer(file)
        for ug in user_group:
            for ug_account_lock in ug['accountLockNotification']:
                row = [
                    ug['ou'],
                    '1',
                    ug_account_lock
                ]
                writer.writerow(row)
            for ug_immediate_login_logout in ug['immediateLoginLogoutNotification']:
                row = [
                    ug['ou'],
                    '2',
                    ug_immediate_login_logout
                ]
                writer.writerow(row)
            for ug_summary_login_logout in ug['summaryLoginLogoutNotification']:
                row = [
                    ug['ou'],
                    '3',
                    ug_summary_login_logout
                ]
                writer.writerow(row)
            for ug_immediate_preapproval in ug['immediatePreapprovalNotification']:
                row = [
                    ug['ou'],
                    '4',
                    ug_immediate_preapproval
                ]
                writer.writerow(row)
            for ug_summary_preapproval in ug['summaryPreapprovalNotification']:
                row = [
                    ug['ou'],
                    '5',
                    ug_summary_preapproval
                ]
                writer.writerow(row)

    with open('user.csv', mode='w', encoding='uft-8', newline='') as file:
        writer = csv.writer(file)
        for u in user:
            ug = find_user_group(u['team'],user_group)
            row = [
                u['uid'],
                u['displayName'],
                u['uidNumber'],
                u['email'],
                ug['ou'],
                u['companyName'] if 'companyName' in u else '',
                u['email2']
            ]
            writer.writerow(row)
    
    with open('user_admin.csv', mode='w', encoding='uft-8', newline='') as file:
        writer = csv.writer(file)
        for u in user:
            if u['idmRole'] == 'IDM_USER_LEADER':
                ug = find_user_group(u['team'],user_group)
                row = [
                    u['uid'],
                    ug['ou']
                ]
                writer.writerow(row)
            else:
                continue