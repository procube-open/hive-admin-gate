#!/usr/bin/python
# -*- coding: utf-8 -*-

import connexion
import six
import os
import openpyxl
import re
from dateutil.parser import parse
import tempfile
import urllib3
from urllib.parse import urlencode
import logging
from distutils.util import strtobool
import subprocess
import json

from swagger_server.models.result import Result  # noqa: E501
from swagger_server.models.file_status import FileStatus  # noqa: E501
from swagger_server.models.spool_list import SpoolList  # noqa: E501
from swagger_server import util

logging.basicConfig(level=(logging.DEBUG if strtobool(os.environ.get('DEBUG', 'False')) else logging.INFO))
logger = logging.getLogger(f'import_controller')
http = urllib3.PoolManager()

# smbclient dir サブコマンド出力サンプル
#   .                                   D        0  Mon Dec 21 03:00:08 2020
#   ..                                  D        0  Mon Dec 21 03:00:08 2020
#   ALL_20201220.txt                    A     7499  Mon Dec 21 03:00:06 2020
#   STOPALL2_20201202.txt               A      395  Wed Dec  2 15:51:32 2020
dir_pattern = re.compile(r'^ *([^ ]+\.xlsx) +A +([^ ]+) +([^ ].*)$')

# smbclient エラーメッセージサンプル
# smbclient "//kiif3-test-win.test.procube.jpx/ExtInfo$" -U 'kiif3_idm%PassWord' -c dir
# do_connect: Connection to kiif3-test-win.test.procube.jpx failed (Error NT_STATUS_UNSUCCESSFUL)
connect_fail_pattern = re.compile(r'do_connect:.*failed')
# smbclient "//kiif3-test-win.test.procube.jp/xExtInfo$" -U 'kiif3_idm%PassWord' -c dir
# tree connect failed: NT_STATUS_BAD_NETWORK_NAME
bad_name_pattern = re.compile(r'NT_STATUS_BAD_NETWORK_NAME')
# smbclient "//kiif3-test-win.test.procube.jp/ExtInfo$" -U 'kiif3_idmx%PassWord' -c dir
# session setup failed: NT_STATUS_LOGON_FAILURE
# smbclient "//kiif3-test-win.test.procube.jp/ExtInfo$" -U 'kiif3_idm%xPassWord' -c dir
# session setup failed: NT_STATUS_LOGON_FAILURE
login_error_pattern = re.compile(r'NT_STATUS_LOGON_FAILURE')
# smbclient "//kiif3-test-win.test.procube.jp/ExtInfo$" -U 'kiif3_idm%PassWord' -c 'get hoge.txt'
# NT_STATUS_OBJECT_NAME_NOT_FOUND opening remote file \hoge.txt
not_found_pattern = re.compile(r'NT_STATUS_OBJECT_NAME_NOT_FOUND')


class SMBClient:
    def __init__(self, path=os.environ['SAMBA_PATH'],
                 user=os.environ['SAMBA_USER'],
                 passwd=os.environ['SAMBA_PASSWORD']):
        self.path = path
        self.user = user
        self.passwd = passwd

    def getErrorMessage(self, stderr, fileName=None):
        if connect_fail_pattern.match(stderr):
            return f'共有フォルダ {self.path} にアクセスしようとしましたが、サーバへの接続に失敗しました'
        if bad_name_pattern.match(stderr):
            return f'共有フォルダ {self.path} にアクセスしようとしましたが、共有名が見つかりませんでした'
        if login_error_pattern.match(stderr):
            return f'共有フォルダ {self.path} にユーザ {self.user} でアクセスしようとしましたが、ログインに失敗しました'
        if not_found_pattern.match(stderr):
            return f'共有フォルダ {self.path} にユーザ {self.user} でアクセスし、ファイル {fileName} を取得しようとしましたが、ファイルが見つかりませんでした'

    def list(self):
        proc = subprocess.run(['smbclient', self.path, '-U', self.user + '%' + self.passwd,
                              '-c', 'dir'], encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            raise RuntimeError(self.getErrorMessage(proc.stderr))
        for line in proc.stdout.splitlines():
            result = dir_pattern.match(line)
            if result:
               yield FileStatus(name=result.group(1), size=result.group(2), mtime=parse(result.group(3)))

    def getBook(self, name):
        with tempfile.TemporaryDirectory() as dirname:
            proc = subprocess.run(['smbclient', self.path, '-U', self.user + '%' + self.passwd,
                                  '-c', 'get ' + name], cwd=dirname, encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if proc.returncode != 0:
                raise RuntimeError(self.getErrorMessage(proc.stderr, fileName=name))
            return openpyxl.load_workbook(dirname + '/' + name)


class IDManager:
    def __init__(self, url='http://localhost:8090/IDManager', user='IDM_ADMIN', group='IDM_ADMIN'):
        # 認証については、呼びもとのユーザを継承する
        self.url = url
        self.user = user
        self.group = group

    def call(self, interface, params=None, key=None, method='GET', data=None):
        url = self.url + '/' + interface
        if key:
            url += '/' + key
        if params:
            url += '?' + urlencode(params)
        headers = {
            'Accept': 'application/json; charset=utf-8',
            'HTTP_REMOTEUSER': self.user,
            'HTTP_REMOTEGROUP': self.group
        }
        if data:
            datastr = json.dumps(data)
            data = datastr.encode('utf-8')
            headers['Content-Type'] = 'application/json; charset=utf-8'
        res = http.request(method, url, body=data, headers=headers)
        # python3 + liburl3 だから json.loads(body, object_hook=_byteify) は不要？
        # https://www.javaer101.com/ja/article/3664748.html
        bodystr = ''
        try:
            bodystr = res.data.decode('utf-8')
            body = json.loads(bodystr)
        except (UnicodeDecodeError, JSONDecodeError):
            body = None
        # 以下のエラーを回避
        # HTTP Error 400: Bad Request: "[{\"code\":\"1100\",\"message\":\"''AES復号化レスポンス使用フラグ''が指定されています。
        # このインタフェースへのリクエスト（参照・追加・更新）が行われた際に、
        # レスポンスオブジェクトのAES暗号化対象属性の値は全て復号化された状態（平文）となります。\",\"level\":\"warn\"}]"'
        if res.status == 200 or (res.status == 400 and
           type(body) == list and any(map(lambda x: type(x) == dict and x.get('code') == '1100', body))):
            return body
        if body:
            # IDManager が body にエラー情報を詰めている場合はそっちを拾う
            raise RuntimeError(f'IDManager でエラーが発生しました。interface={interface} data={datastr} error={bodystr}')
        raise RuntimeError(f'IDManager の  API 呼び出しで HTTP エラーが発生しました:status={res.status}')

    def get(self, interface, key=None, params=None):
        return self.call(interface, key=key, params=params)

    def update(self, interface, key, data, params=None):
        return self.call(interface, key=key, params=params, data=data, method='PUT')

    def create(self, interface, data, params=None):
        return self.call(interface, params=params, data=data, method='POST')

    def commit(self, rollback=False):
        response = self.get('_currentSandboxProvRequestsUser', key=self.user)
        if not response:
            logger.info("No provisioning Request found for {0}.".format(self.user))
            return
        request_id = response[0]['id']
        logger.info(f'Success to get provisiong request for {self.user} id={request_id}')
        data = dict(requestId=request_id)
        if rollback:
            data['cancel'] = True
        response = self.create('_editingCompletedEvents', data)
        logger.info('Success to commit/cancel provisiong request {data}')


jinji_select = {
    'selectOld': False,
    'selectNext': False,
    'selectJinji': True,
    'selectInput': False
}


class Context:
    def __init__(self, file_name, user, group):
        self.staff_table = dict()
        self.staff_table['1'] = dict()
        self.staff_table['2'] = dict()
        self.summery = dict()
        self.target_count = 0
        self.count = 0
        self.first_time_count = 0
        self.create_count = 0
        self.update_count = 0
        self.delete_count = 0
        self.file_name = file_name
        self.user = user
        self.group = group
        self.inserts = []
        self.updates = []

    def load_all_staff(self, idm):
        self.all_staff = idm.get('importJinjiTransfer')
        self.target_count = len(self.all_staff)

    def build_table(self):
        for staff in self.all_staff:
            if 'employmentType' in staff and 'employeeNumber' in staff:
                self.staff_table['1' if staff['employmentType'] == '1' else '2'][staff['employeeNumber']] = staff
        self.all_staff = None

    def merge_jinji(self, jinji_staff):
        first_time = True
        if jinji_staff['employeeNumber'] in self.staff_table[jinji_staff['employmentType']]:
            staff = self.staff_table[jinji_staff['employmentType']][jinji_staff['employeeNumber']]
            jinji_belong_code = staff.get('jinjiBelongCode', '')
            jinji_job_category_code = staff.get('jinjiJobCategoryCode', '')
            jinji_appointment_code = staff.get('jinjiAppointmentCode', '')
            jinji_leave_code = staff.get('jinjiLeaveCode', '')
            work_flow_phase1 = staff.get('leaveWF1', '')
            work_flow_phase2 = staff.get('leaveWF2', '')
            # jinji 3属性に変化がない場合は update を行わない
            if (jinji_belong_code != jinji_staff['jinjiBelongCode'] or jinji_job_category_code != jinji_staff['jinjiJobCategoryCode'] or
               jinji_appointment_code != jinji_staff['jinjiAppointmentCode'] or jinji_leave_code != jinji_staff['jinjiLeaveCode']):
                staff['jinjiBelongCode'] = jinji_staff['jinjiBelongCode']
                staff['jinjiJobCategoryCode'] = jinji_staff['jinjiJobCategoryCode']
                staff['jinjiAppointmentCode'] = jinji_staff['jinjiAppointmentCode']
                staff['jinjiLeaveCode'] = jinji_staff['jinjiLeaveCode']
                # 以下はIDM初期化式で設定
                staff.pop('jinjiOrganization', None)
                staff.pop('jinjiJobCode', None)
                staff.pop('jinjiJobTitle', None)
                staff.pop('jinjiUserPosition', None)
                staff.pop('jinjiPermission', None)
                if jinji_staff['employmentType'] == '1' and not(jinji_belong_code or jinji_job_category_code or jinji_appointment_code or jinji_leave_code):
                    # 正規職員の初回取り込みの際は人給選択をチェック
                    staff.update(jinji_select)
                    self.first_time_count += 1
                elif jinji_staff['employmentType'] != '1' and not(jinji_belong_code or jinji_job_category_code or jinji_appointment_code or jinji_leave_code or work_flow_phase1 or work_flow_phase2):
                    # 臨時職員の初回取り込みかつ様式19が未取り込みの場合は人給選択をチェック
                    staff.update(jinji_select)
                    self.first_time_count += 1
                else:
                    self.update_count += 1
                self.updates.append(staff)
            del self.staff_table[jinji_staff['employmentType']][jinji_staff['employeeNumber']]
        else:
            # 新規レコード作成
            if jinji_staff['employeeNumber'] == '1':
                jinji_staff.update(jinji_select)
            self.inserts.append(jinji_staff)
            self.create_count += 1
        self.count += 1

    def collect_deletes(self):
        for staff in self.staff_table['1'].values():
            staff.pop('jinjiBelongCode', None)
            staff.pop('jinjiJobCategoryCode', None)
            staff.pop('jinjiAppointmentCode', None)
            staff.pop('jinjiLeaveCode', None)
            self.delete_count += 1
        for staff in self.staff_table['1'].values():
            staff.pop('jinjiBelongCode', None)
            staff.pop('jinjiJobCategoryCode', None)
            staff.pop('jinjiAppointmentCode', None)
            staff.pop('jinjiLeaveCode', None)
            self.delete_count += 1

    def update_all(self, idm):
        for staff in self.updates:
            idm.update('importJinjiTransfer', staff['id'], staff)

    def insert_all(self, idm):
        for staff in self.inserts:
            idm.create('importJinjiTransfer', staff)

    def summery_dumps(self):
        s1 = f'count={self.count} target_count={self.target_count} first_time_count={self.first_time_count}'
        s2 = f' create_count={self.create_count} update_count={self.update_count} delete_count={self.delete_count}'
        return s1 + s2

class phase:
    def __init__(self, context):
        self.context = context

    def run(self):
        logger.info(f'Start {self.__class__.__name__} phase.')
        self.do()
        logger.info(f'End {self.__class__.__name__} phase {self.context.summery_dumps()}.')


class readAllStaff(phase):
    def do(self):
        idm = IDManager(user=self.context.user, group=self.context.group)
        self.context.load_all_staff(idm)


class buildTable(phase):
    def do(self):
        self.context.build_table()


# Excel ヘッダマップ
# 0:★職員番号   1:★旧職員番号  2:★氏名  3:★カナ氏名  4:★旧姓  5:★カナ旧姓  6:★旧姓使用申請区分
# 7:★給与所属コード［＊］  8:★給与所属名称  9:★校種コード［＊］  10:★校種コード  11:★職員種別［＊］
# 12:★職員種別  13:★短時間勤務区分［＊］  14:★短時間勤務区分  15:★職種名コード［＊］  16:★職種名称
# 17:★職名コード［＊］  18:★職名名称  19:★補職名コード［＊］ 20:★補職名称  21:★育児短時間区分［＊］
# 22:★育児短時間区分  23:★休退コード［＊］  24:★休退コード  25:発令日付（辞令日）  26:発令区分［＊］
# 27:発令区分名称  28:発令内容区分［＊］  29:発令内容名称
def row2dict(row):
    logger.info(f'row[0].value={row[0].value}')
    if not row[0].value:
        raise RuntimeError(f'読み込んだファイルの行{row[0].row}のA列：職員番号が空です')
    employmentType = row[11].value
    if employmentType == None or employmentType == '':
        raise RuntimeError(f'読み込んだファイルの行{row[0].row}のL列：職員種別コードが空です')
    try:
        employmentType = int(employmentType)
    except (TypeError, ValueError):
        raise RuntimeError(f'読み込んだファイルの行{row[0].row}のL列：職員種別コードの値{employmentType}が数値ではありません')
    if employmentType < 1:
        raise RuntimeError(f'読み込んだファイルの行{row[0].row}のL列：職員種別コードに1より小さい値{employmentType}は指定できません。')
    data = {
        'employeeNumber': cell2str(row[0]),
        'employmentType': '1' if employmentType == 1 else '2',
    }
    if has_value(row[6]):
        if has_value(row[2]):
            data['fullNameKanji'] = cell2str(row[4])
        if has_value(row[3]):
            data['fullNameKana'] = cell2str(row[5])
    else:
        if has_value(row[2]):
            data['fullNameKanji'] = cell2str(row[2])
        if has_value(row[3]):
            data['fullNameKana'] = cell2str(row[3])
    data['jinjiBelongCode'] = cell2str(row[7]).zfill(4)
    data['jinjiJobCategoryCode'] = cell2str(row[15]).zfill(3)
    data['jinjiAppointmentCode'] = cell2str(row[19])
    data['jinjiLeaveCode'] = cell2str(row[24])
    return data

def cell2str(cell):
    return '' if cell.value is None else str(cell.value).strip()

def has_value(cell):
    return cell.value and str(cell.value).strip()

class readExcel(phase):
    def do(self):
        wb = SMBClient().getBook(self.context.file_name)
        ws = wb.worksheets[0]
        header = True
        data = []
        for row in ws.rows:
            if header:
                header = False
            elif any(has_value(c) for c in row):
                self.context.merge_jinji(row2dict(row))
        self.context.collect_deletes()

class importToIDM(phase):
    def do(self):
        idm = IDManager(user=self.context.user, group=self.context.group)
        self.context.update_all(idm)
        self.context.insert_all(idm)


class commit(phase):
    def do(self):
        idm = IDManager(user=self.context.user, group=self.context.group)
        idm.commit()


class rollback(phase):
    def do(self):
        idm = IDManager(user=self.context.user, group=self.context.group)
        idm.commit(rollback=True)


def import_file(name, action, http_remoteuser=None, http_remotegroup=None):  # noqa: E501
    """ファイルをインポートする

    人給の Excel ファイルを読み込んで ID Manager にインポートする # noqa: E501

    :param name: ファイル名
    :type name: str
    :param action: ファイルに対するアクションを指定する。import を指定すると、対象となるファイルをID Manager に
                   インポートする。summery を指定するとインポートした場合に発生する変更件数をカウントして返す。
    :type action: str
    :param http_remoteuser: IDManager にアクセスする際のユーザID。ただし、前段の WebGate で設定されるため、
                            REST APIとして呼び出す側はこのヘッダーを設定してはならない。
    :type http_remoteuser: str
    :param http_remotegroup: IDManager にアクセスする際のグループID。ただし、前段の WebGate で設定されるため、
                             REST APIとして呼び出す側はこのヘッダーを設定してはならない。
    :type http_remotegroup: str

    :rtype: Result
    """

    # Header Parameter は connexion ではサポートされていない
    # https://connexion.readthedocs.io/en/latest/request.html#header-parameters
    context = Context(name, connexion.request.headers['HTTP_REMOTEUSER'], connexion.request.headers['HTTP_REMOTEGROUP'])
    try:
        readAllStaff(context).run()
        buildTable(context).run()
        readExcel(context).run()
        if action == 'import':
            try:
                importToIDM(context).run()
                commit(context).run()
            except Exception as e:
                rollback(context).run()
                raise e
    except Exception as err:
        logger.exception('Error: %s', err)
        return Result(result='failed', failed_data=str(err))
    return Result(result='completed', count=context.count, target_count=context.target_count,
           first_time_count=context.first_time_count, update_count=context.update_count, delete_count=context.delete_count)


def list_spool(http_remoteuser=None, http_remotegroup=None):   # noqa: E501
    """ファイルの一覧を取得する

    ファイルの一覧を取得する # noqa: E501

    :param http_remoteuser: IDManager にアクセスする際のユーザID。ただし、前段の WebGate で設定されるため、
                            REST APIとして呼び出す側はこのヘッダーを設定してはならない。
    :type http_remoteuser: str
    :param http_remotegroup: IDManager にアクセスする際のグループID。ただし、前段の WebGate で設定されるため、
                             REST APIとして呼び出す側はこのヘッダーを設定してはならない。
    :type http_remotegroup: str

    :rtype: SpoolList
    """
    try:
        return SpoolList(result='completed', data=list(SMBClient().list()))
    except Exception as e:
        logger.exception('Error: %s', e)
        return SpoolList(result='failed', failed_data=f'Error: {e}')
