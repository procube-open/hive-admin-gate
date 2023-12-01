# クラス定義

本システムで ID Manager に定義されているクラスについて説明します。

## LDAP汎用オブジェクト(LdapGenericObject)
クラスのキー属性はdn です。
このクラスの属性は以下のとおりです。
### DN(dn)
DN(dn) はLDAPのディレクトリーツリー内での位置を示す識別子です。
| データ型|string|
|----|----------------|
|必須|:o:|
|一意|:o:（大文字小文字無視）|
| 最大長|1024|
| 最小長|1|
### オブジェクトクラス(objectClass)
オブジェクトクラス(objectClass) はLDAPのオブジェクトクラスです。
| データ型|stringの配列|
|----|----------------|
|必須|:x:|
|一意|:x:|
| 最大長|1024|
| 最小長|1|
### DC(dc)
DC(dc) はドメインコンポーネントです。
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
| 最大長|256|
| 最小長|1|
### CN(cn)
CN(cn) は一般名称です。
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
| 最大長|256|
| 最小長|1|
### SN(sn)
SN(sn) は姓です。
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
| 最大長|256|
| 最小長|1|
### OU(ou)
OU(ou) は組織単位です。
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
| 最大長|256|
| 最小長|1|
### パスワード(userPassword)
パスワード(userPassword) はユーザのパスワードです。
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### UID(uid)
UID(uid) はユーザIDです。
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
| 最大長|256|
| 最小長|1|
### オブジェクトレベル(level)
| データ型|number|
|----|----------------|
|必須|:x:|
|一意|:x:|
## 接続先(connection)
クラスのキー属性はname です。
このクラスの属性は以下のとおりです。
### 接続先名(name)
| データ型|string|
|----|----------------|
|必須|:o:|
|一意|:o:|
### 接続機器(machine)
| データ型|string|
|----|----------------|
|必須|:o:|
|一意|:x:|
### プロトコル(protocol)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### ポート(port)
| データ型|number|
|----|----------------|
|必須|:o:|
|一意|:x:|
## 接続先グループ(connectionGroup)
クラスのキー属性はname です。
このクラスの属性は以下のとおりです。
### 接続先グループ名(name)
| データ型|string|
|----|----------------|
|必須|:o:|
|一意|:o:|
### 接続先一覧(connections)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
## 連携システムオブジェクト(linkageSystem)
クラスのキー属性はsystemId です。
このクラスの属性は以下のとおりです。
### システムID(systemId)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### 鍵(key)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
## 機器(machine)
クラスのキー属性はname です。
このクラスの属性は以下のとおりです。
### 機器名(name)
| データ型|string|
|----|----------------|
|必須|:o:|
|一意|:o:|
### ホスト名(hostname)
| データ型|string|
|----|----------------|
|必須|:o:|
|一意|:o:|
### 接続先一覧(connections)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### 認証ユーザー(certificationUser)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### 認証パスワード(certificationPassword)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
## SAML属性定義(samlattr)
このクラスは内包オブジェクトです。
このクラスの属性は以下のとおりです。
### 属性定義ID(attr_id)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### 属性(attr)
属性(attr) はE/U管理者画面には「連携項目名」として表示です。
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
## SAML NameID定義(samlnameid)
このクラスは内包オブジェクトです。
このクラスの属性は以下のとおりです。
### NameIDフォーマット(nameid_format)
| データ型|string|
|----|----------------|
|必須|:o:|
|一意|:x:|
### SAML属性ID(attr_id)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
## SAML SP(samlsp)
このクラスは内包オブジェクトです。
このクラスの属性は以下のとおりです。
### 公開名(published_name)
公開名(published_name) はSPのシステムを一位に特定するための名称です。
| データ型|string|
|----|----------------|
|必須|:o:|
|一意|:x:|
### SP メタデータ(metadata)
SP メタデータ(metadata) はSAML  SP のメタデータです。
| データ型|string|
|----|----------------|
|必須|:o:|
|一意|:x:|
### サービスURL(service_url)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### 配信対象SAML属性(saml_attrs_for_delivery)
| データ型|stringの配列|
|----|----------------|
|必須|:x:|
|一意|:x:|
### SAMLアサーションを暗号化する(encryptAssertions)
SAMLアサーションを暗号化する(encryptAssertions) はIdPからSPに送るSAMLアサーションを暗号化する。 Office 365の場合は false を設定する。です。
| データ型|boolean|
|----|----------------|
|必須|:x:|
|一意|:x:|
### 応答に署名する(signResponses)
応答に署名する(signResponses) はIdPからSPに送る応答に署名する。Office365の場合は  false を指定する。です。
| データ型|boolean|
|----|----------------|
|必須|:x:|
|一意|:x:|
### SAMLアサーションに署名する(signAssertions)
SAMLアサーションに署名する(signAssertions) はIdPからSPに送るSAMLアサーションに署名する。Office365の場合は true を指定する。です。
| データ型|boolean|
|----|----------------|
|必須|:x:|
|一意|:x:|
## 利用者(user)
クラスのキー属性はuid です。
このクラスでは対応する LDAP スキーマが自動的に設定されます。
LDAPスキーマの親クラスは person です。
このクラスの属性は以下のとおりです。
### ユーザID(uid)
ユーザID(uid) はユーザを識別する一意の IDです。
| データ型|string|
|----|----------------|
|必須|:o:|
|一意|:o:（大文字小文字無視）|
| 最大長|64|
| 最小長|1|
### 氏名(cn)
氏名(cn) はユーザの氏名です。
| データ型|string|
|----|----------------|
|必須|:o:|
|一意|:x:|
| 最大長|256|
| 最小長|1|
### ID管理役割(idmRole)
ID管理役割(idmRole) はユーザがID管理業務上割り当てられた役割です。
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### パスワード(userPassword)
パスワード(userPassword) は	ユーザのパスワードです。
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### DN(dn)
DN(dn) はLDAPのディレクトリーツリー内での位置を示す識別子です。
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### アカウント無効化(accountLock)
アカウント無効化(accountLock) はtrue の場合アカウントを無効化するです。
| データ型|boolean|
|----|----------------|
|必須|:x:|
|一意|:x:|
### データ1(data1)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### データ2(data2)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### データ3(data3)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### データ4(data4)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### データ5(data5)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
## 利用者グループ(userGroups)
クラスのキー属性はname です。
このクラスの属性は以下のとおりです。
### グループ名(name)
グループ名(name) は利用者グループのグループ名を入力してください。です。
| データ型|string|
|----|----------------|
|必須|:o:|
|一意|:o:|
### 利用者一覧(users)
| データ型|stringの配列|
|----|----------------|
|必須|:x:|
|一意|:x:|
## 作業(work)
クラスのキー属性はid です。
このクラスの属性は以下のとおりです。
### 業務ID(id)
| データ型|string|
|----|----------------|
|必須|:o:|
|一意|:o:|
### 業務名(name)
| データ型|string|
|----|----------------|
|必須|:o:|
|一意|:o:|
### 開始日時(startDatetime)
| データ型|datetime|
|----|----------------|
|必須|:o:|
|一意|:x:|
### 終了日時(endDatetime)
| データ型|datetime|
|----|----------------|
|必須|:x:|
|一意|:x:|
### ステータス(status)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### ユーザー(users)
| データ型|stringの配列|
|----|----------------|
|必須|:x:|
|一意|:x:|
### ユーザーグループ(userGroups)
| データ型|stringの配列|
|----|----------------|
|必須|:x:|
|一意|:x:|
### 接続先(connections)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### 接続先グループ(connectionGroups)
| データ型|stringの配列|
|----|----------------|
|必須|:x:|
|一意|:x:|
### 申請者(applicationUser)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### 申請日時(applicationDatetime)
| データ型|datetime|
|----|----------------|
|必須|:x:|
|一意|:x:|
### 申請者コメント(applicationComment)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### 承認者(approvedUser)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|
### 承認日時(approvedDatetime)
| データ型|datetime|
|----|----------------|
|必須|:x:|
|一意|:x:|
### 承認者コメント(applovedComment)
| データ型|string|
|----|----------------|
|必須|:x:|
|一意|:x:|