# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from task_executer.models.base_model_ import Model
from task_executer.models.enum_definition import EnumDefinition
from task_executer.models.propagation_setting import PropagationSetting
import re
from task_executer import util

from task_executer.models.enum_definition import EnumDefinition  # noqa: E501
from task_executer.models.propagation_setting import PropagationSetting  # noqa: E501
import re  # noqa: E501

class PropertyDefinition(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, name=None, display_name=None, type=None, class_name=None, is_array=None, description=None, required=None, values=None, values_ex=None, values_interface=None, allow_another_value=None, unique=None, unique_ignore_case=None, string_restriction=None, max_len=None, min_len=None, pattern=None, pattern_for_input=None, prop_group_name=None, derivation=None, propagations=None, encryption=None, output_ldap_schema=None):  # noqa: E501
        """PropertyDefinition - a model defined in OpenAPI

        :param name: The name of this PropertyDefinition.  # noqa: E501
        :type name: str
        :param display_name: The display_name of this PropertyDefinition.  # noqa: E501
        :type display_name: str
        :param type: The type of this PropertyDefinition.  # noqa: E501
        :type type: str
        :param class_name: The class_name of this PropertyDefinition.  # noqa: E501
        :type class_name: str
        :param is_array: The is_array of this PropertyDefinition.  # noqa: E501
        :type is_array: bool
        :param description: The description of this PropertyDefinition.  # noqa: E501
        :type description: str
        :param required: The required of this PropertyDefinition.  # noqa: E501
        :type required: bool
        :param values: The values of this PropertyDefinition.  # noqa: E501
        :type values: List[EnumDefinition]
        :param values_ex: The values_ex of this PropertyDefinition.  # noqa: E501
        :type values_ex: str
        :param values_interface: The values_interface of this PropertyDefinition.  # noqa: E501
        :type values_interface: str
        :param allow_another_value: The allow_another_value of this PropertyDefinition.  # noqa: E501
        :type allow_another_value: bool
        :param unique: The unique of this PropertyDefinition.  # noqa: E501
        :type unique: bool
        :param unique_ignore_case: The unique_ignore_case of this PropertyDefinition.  # noqa: E501
        :type unique_ignore_case: bool
        :param string_restriction: The string_restriction of this PropertyDefinition.  # noqa: E501
        :type string_restriction: str
        :param max_len: The max_len of this PropertyDefinition.  # noqa: E501
        :type max_len: int
        :param min_len: The min_len of this PropertyDefinition.  # noqa: E501
        :type min_len: int
        :param pattern: The pattern of this PropertyDefinition.  # noqa: E501
        :type pattern: str
        :param pattern_for_input: The pattern_for_input of this PropertyDefinition.  # noqa: E501
        :type pattern_for_input: str
        :param prop_group_name: The prop_group_name of this PropertyDefinition.  # noqa: E501
        :type prop_group_name: List[str]
        :param derivation: The derivation of this PropertyDefinition.  # noqa: E501
        :type derivation: str
        :param propagations: The propagations of this PropertyDefinition.  # noqa: E501
        :type propagations: List[PropagationSetting]
        :param encryption: The encryption of this PropertyDefinition.  # noqa: E501
        :type encryption: str
        :param output_ldap_schema: The output_ldap_schema of this PropertyDefinition.  # noqa: E501
        :type output_ldap_schema: bool
        """
        self.openapi_types = {
            'name': str,
            'display_name': str,
            'type': str,
            'class_name': str,
            'is_array': bool,
            'description': str,
            'required': bool,
            'values': List[EnumDefinition],
            'values_ex': str,
            'values_interface': str,
            'allow_another_value': bool,
            'unique': bool,
            'unique_ignore_case': bool,
            'string_restriction': str,
            'max_len': int,
            'min_len': int,
            'pattern': str,
            'pattern_for_input': str,
            'prop_group_name': List[str],
            'derivation': str,
            'propagations': List[PropagationSetting],
            'encryption': str,
            'output_ldap_schema': bool
        }

        self.attribute_map = {
            'name': 'name',
            'display_name': 'displayName',
            'type': 'type',
            'class_name': 'className',
            'is_array': 'isArray',
            'description': 'description',
            'required': 'required',
            'values': 'values',
            'values_ex': 'valuesEx',
            'values_interface': 'valuesInterface',
            'allow_another_value': 'allowAnotherValue',
            'unique': 'unique',
            'unique_ignore_case': 'uniqueIgnoreCase',
            'string_restriction': 'stringRestriction',
            'max_len': 'maxLen',
            'min_len': 'minLen',
            'pattern': 'pattern',
            'pattern_for_input': 'patternForInput',
            'prop_group_name': 'propGroupName',
            'derivation': 'derivation',
            'propagations': 'propagations',
            'encryption': 'encryption',
            'output_ldap_schema': 'outputLdapSchema'
        }

        self._name = name
        self._display_name = display_name
        self._type = type
        self._class_name = class_name
        self._is_array = is_array
        self._description = description
        self._required = required
        self._values = values
        self._values_ex = values_ex
        self._values_interface = values_interface
        self._allow_another_value = allow_another_value
        self._unique = unique
        self._unique_ignore_case = unique_ignore_case
        self._string_restriction = string_restriction
        self._max_len = max_len
        self._min_len = min_len
        self._pattern = pattern
        self._pattern_for_input = pattern_for_input
        self._prop_group_name = prop_group_name
        self._derivation = derivation
        self._propagations = propagations
        self._encryption = encryption
        self._output_ldap_schema = output_ldap_schema

    @classmethod
    def from_dict(cls, dikt) -> 'PropertyDefinition':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The _propertyDefinition of this PropertyDefinition.  # noqa: E501
        :rtype: PropertyDefinition
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self):
        """Gets the name of this PropertyDefinition.

        属性の名前  # noqa: E501

        :return: The name of this PropertyDefinition.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PropertyDefinition.

        属性の名前  # noqa: E501

        :param name: The name of this PropertyDefinition.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if name is not None and not re.search(r'^[A-Za-z][0-9A-Za-z_]*$', name):  # noqa: E501
            raise ValueError("Invalid value for `name`, must be a follow pattern or equal to `/^[A-Za-z][0-9A-Za-z_]*$/`")  # noqa: E501

        self._name = name

    @property
    def display_name(self):
        """Gets the display_name of this PropertyDefinition.

        属性の表示名。省略時には、名前が表示される。  # noqa: E501

        :return: The display_name of this PropertyDefinition.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this PropertyDefinition.

        属性の表示名。省略時には、名前が表示される。  # noqa: E501

        :param display_name: The display_name of this PropertyDefinition.
        :type display_name: str
        """

        self._display_name = display_name

    @property
    def type(self):
        """Gets the type of this PropertyDefinition.

        属性のデータ型  # noqa: E501

        :return: The type of this PropertyDefinition.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this PropertyDefinition.

        属性のデータ型  # noqa: E501

        :param type: The type of this PropertyDefinition.
        :type type: str
        """
        allowed_values = ["string", "boolean", "number", "float", "datetime", "date", "ipaddress", "object"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def class_name(self):
        """Gets the class_name of this PropertyDefinition.

        属性のデータ型がオブジェクトである場合に格納されるオブジェクトのクラス名  # noqa: E501

        :return: The class_name of this PropertyDefinition.
        :rtype: str
        """
        return self._class_name

    @class_name.setter
    def class_name(self, class_name):
        """Sets the class_name of this PropertyDefinition.

        属性のデータ型がオブジェクトである場合に格納されるオブジェクトのクラス名  # noqa: E501

        :param class_name: The class_name of this PropertyDefinition.
        :type class_name: str
        """

        self._class_name = class_name

    @property
    def is_array(self):
        """Gets the is_array of this PropertyDefinition.

        属性が複数値を持つか否かを示す  # noqa: E501

        :return: The is_array of this PropertyDefinition.
        :rtype: bool
        """
        return self._is_array

    @is_array.setter
    def is_array(self, is_array):
        """Sets the is_array of this PropertyDefinition.

        属性が複数値を持つか否かを示す  # noqa: E501

        :param is_array: The is_array of this PropertyDefinition.
        :type is_array: bool
        """

        self._is_array = is_array

    @property
    def description(self):
        """Gets the description of this PropertyDefinition.

        属性の説明 ガジェット上で、この属性の入力コントロールにフォーカスされたときに説明文として表示される  # noqa: E501

        :return: The description of this PropertyDefinition.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this PropertyDefinition.

        属性の説明 ガジェット上で、この属性の入力コントロールにフォーカスされたときに説明文として表示される  # noqa: E501

        :param description: The description of this PropertyDefinition.
        :type description: str
        """

        self._description = description

    @property
    def required(self):
        """Gets the required of this PropertyDefinition.

        この属性が必須であることを示す  # noqa: E501

        :return: The required of this PropertyDefinition.
        :rtype: bool
        """
        return self._required

    @required.setter
    def required(self, required):
        """Sets the required of this PropertyDefinition.

        この属性が必須であることを示す  # noqa: E501

        :param required: The required of this PropertyDefinition.
        :type required: bool
        """

        self._required = required

    @property
    def values(self):
        """Gets the values of this PropertyDefinition.


        :return: The values of this PropertyDefinition.
        :rtype: List[EnumDefinition]
        """
        return self._values

    @values.setter
    def values(self, values):
        """Sets the values of this PropertyDefinition.


        :param values: The values of this PropertyDefinition.
        :type values: List[EnumDefinition]
        """

        self._values = values

    @property
    def values_ex(self):
        """Gets the values_ex of this PropertyDefinition.

        属性がとり得る値を定義する列挙オブジェクトの配列を返す計算式。列挙値と同時に指定された場合は、マージした結果が列挙値となる。  # noqa: E501

        :return: The values_ex of this PropertyDefinition.
        :rtype: str
        """
        return self._values_ex

    @values_ex.setter
    def values_ex(self, values_ex):
        """Sets the values_ex of this PropertyDefinition.

        属性がとり得る値を定義する列挙オブジェクトの配列を返す計算式。列挙値と同時に指定された場合は、マージした結果が列挙値となる。  # noqa: E501

        :param values_ex: The values_ex of this PropertyDefinition.
        :type values_ex: str
        """

        self._values_ex = values_ex

    @property
    def values_interface(self):
        """Gets the values_interface of this PropertyDefinition.

        多数のオブジェクトから属性の値を選択するためのリストを取得するインタフェース  # noqa: E501

        :return: The values_interface of this PropertyDefinition.
        :rtype: str
        """
        return self._values_interface

    @values_interface.setter
    def values_interface(self, values_interface):
        """Sets the values_interface of this PropertyDefinition.

        多数のオブジェクトから属性の値を選択するためのリストを取得するインタフェース  # noqa: E501

        :param values_interface: The values_interface of this PropertyDefinition.
        :type values_interface: str
        """

        self._values_interface = values_interface

    @property
    def allow_another_value(self):
        """Gets the allow_another_value of this PropertyDefinition.

        属性がとり得る値が列挙値や列挙値式で限定されいてる場合に、別の値が許容されるか否かを示す。特に属性が他のオブジェクトの ID を含むような場合に、列挙値式でそのリンク関係を表現し、この値を false にすることでリンク切れを禁止することができる。 - false の場合、ユーザインタフェース上はドロップダウンリストなどで入力値が制限されるが、 API 上もサーバ側でチェックされる。  # noqa: E501

        :return: The allow_another_value of this PropertyDefinition.
        :rtype: bool
        """
        return self._allow_another_value

    @allow_another_value.setter
    def allow_another_value(self, allow_another_value):
        """Sets the allow_another_value of this PropertyDefinition.

        属性がとり得る値が列挙値や列挙値式で限定されいてる場合に、別の値が許容されるか否かを示す。特に属性が他のオブジェクトの ID を含むような場合に、列挙値式でそのリンク関係を表現し、この値を false にすることでリンク切れを禁止することができる。 - false の場合、ユーザインタフェース上はドロップダウンリストなどで入力値が制限されるが、 API 上もサーバ側でチェックされる。  # noqa: E501

        :param allow_another_value: The allow_another_value of this PropertyDefinition.
        :type allow_another_value: bool
        """

        self._allow_another_value = allow_another_value

    @property
    def unique(self):
        """Gets the unique of this PropertyDefinition.

        一意性が true の場合、コレクション内のすべてのオブジェクトについて、この属性の値が一意であることを示す。ただし、オブジェクトが object[] の属性内のオブジェクトである場合は、その配列の中で一意となる。  # noqa: E501

        :return: The unique of this PropertyDefinition.
        :rtype: bool
        """
        return self._unique

    @unique.setter
    def unique(self, unique):
        """Sets the unique of this PropertyDefinition.

        一意性が true の場合、コレクション内のすべてのオブジェクトについて、この属性の値が一意であることを示す。ただし、オブジェクトが object[] の属性内のオブジェクトである場合は、その配列の中で一意となる。  # noqa: E501

        :param unique: The unique of this PropertyDefinition.
        :type unique: bool
        """

        self._unique = unique

    @property
    def unique_ignore_case(self):
        """Gets the unique_ignore_case of this PropertyDefinition.

        一意性チェック時に大文字小文字を無視するかどうかを示す。 true の場合、この属性の値が大文字小文字を区別せずに一意であることを示す。  # noqa: E501

        :return: The unique_ignore_case of this PropertyDefinition.
        :rtype: bool
        """
        return self._unique_ignore_case

    @unique_ignore_case.setter
    def unique_ignore_case(self, unique_ignore_case):
        """Sets the unique_ignore_case of this PropertyDefinition.

        一意性チェック時に大文字小文字を無視するかどうかを示す。 true の場合、この属性の値が大文字小文字を区別せずに一意であることを示す。  # noqa: E501

        :param unique_ignore_case: The unique_ignore_case of this PropertyDefinition.
        :type unique_ignore_case: bool
        """

        self._unique_ignore_case = unique_ignore_case

    @property
    def string_restriction(self):
        """Gets the string_restriction of this PropertyDefinition.

        使用できる文字種および文字列パターンの限定。  # noqa: E501

        :return: The string_restriction of this PropertyDefinition.
        :rtype: str
        """
        return self._string_restriction

    @string_restriction.setter
    def string_restriction(self, string_restriction):
        """Sets the string_restriction of this PropertyDefinition.

        使用できる文字種および文字列パターンの限定。  # noqa: E501

        :param string_restriction: The string_restriction of this PropertyDefinition.
        :type string_restriction: str
        """
        allowed_values = ["id", "hiragana", "katakana", "password", "macaddr", "mailaddr", "systemid", "formula", "query", "regexp", "dn"]  # noqa: E501
        if string_restriction not in allowed_values:
            raise ValueError(
                "Invalid value for `string_restriction` ({0}), must be one of {1}"
                .format(string_restriction, allowed_values)
            )

        self._string_restriction = string_restriction

    @property
    def max_len(self):
        """Gets the max_len of this PropertyDefinition.

        属性の値の最大長 - WebUI でのチェック - LDAPスキーマや RDBスキーマの生成時にデータ型として出力 - Validateチェック - ヘルプの生成  # noqa: E501

        :return: The max_len of this PropertyDefinition.
        :rtype: int
        """
        return self._max_len

    @max_len.setter
    def max_len(self, max_len):
        """Sets the max_len of this PropertyDefinition.

        属性の値の最大長 - WebUI でのチェック - LDAPスキーマや RDBスキーマの生成時にデータ型として出力 - Validateチェック - ヘルプの生成  # noqa: E501

        :param max_len: The max_len of this PropertyDefinition.
        :type max_len: int
        """

        self._max_len = max_len

    @property
    def min_len(self):
        """Gets the min_len of this PropertyDefinition.

        属性の値の最小長 - WebUI でのチェック - LDAPスキーマや RDBスキーマの生成時にデータ型として出力 - Validateチェック - ヘルプの生成  # noqa: E501

        :return: The min_len of this PropertyDefinition.
        :rtype: int
        """
        return self._min_len

    @min_len.setter
    def min_len(self, min_len):
        """Sets the min_len of this PropertyDefinition.

        属性の値の最小長 - WebUI でのチェック - LDAPスキーマや RDBスキーマの生成時にデータ型として出力 - Validateチェック - ヘルプの生成  # noqa: E501

        :param min_len: The min_len of this PropertyDefinition.
        :type min_len: int
        """

        self._min_len = min_len

    @property
    def pattern(self):
        """Gets the pattern of this PropertyDefinition.

        この属性の文字種および文字列パターンのデータベース格納値を制約するための正規表現。本属性の値（MACアドレスなどの場合には正規化後の値）の全部または一部がこの正規表現にマッチすれば、許可される。完全一致が必要な場合には、先頭と末尾を指定した正規表現を記述しなければならない。本属性の値が設定されない場合には格納値の正規表現チェックは実行されない  # noqa: E501

        :return: The pattern of this PropertyDefinition.
        :rtype: str
        """
        return self._pattern

    @pattern.setter
    def pattern(self, pattern):
        """Sets the pattern of this PropertyDefinition.

        この属性の文字種および文字列パターンのデータベース格納値を制約するための正規表現。本属性の値（MACアドレスなどの場合には正規化後の値）の全部または一部がこの正規表現にマッチすれば、許可される。完全一致が必要な場合には、先頭と末尾を指定した正規表現を記述しなければならない。本属性の値が設定されない場合には格納値の正規表現チェックは実行されない  # noqa: E501

        :param pattern: The pattern of this PropertyDefinition.
        :type pattern: str
        """

        self._pattern = pattern

    @property
    def pattern_for_input(self):
        """Gets the pattern_for_input of this PropertyDefinition.

        この属性の文字種および文字列パターンの入力値を制約するための正規表現。本属性の値（登録・更新リクエストで指定された値）の全部または一部がこの正規表現にマッチすれば、許可される。完全一致が必要な場合には、先頭と末尾を指定した正規表現を記述しなければならない。本属性の値が設定されない場合には入力値の正規表現チェックは実行されない  # noqa: E501

        :return: The pattern_for_input of this PropertyDefinition.
        :rtype: str
        """
        return self._pattern_for_input

    @pattern_for_input.setter
    def pattern_for_input(self, pattern_for_input):
        """Sets the pattern_for_input of this PropertyDefinition.

        この属性の文字種および文字列パターンの入力値を制約するための正規表現。本属性の値（登録・更新リクエストで指定された値）の全部または一部がこの正規表現にマッチすれば、許可される。完全一致が必要な場合には、先頭と末尾を指定した正規表現を記述しなければならない。本属性の値が設定されない場合には入力値の正規表現チェックは実行されない  # noqa: E501

        :param pattern_for_input: The pattern_for_input of this PropertyDefinition.
        :type pattern_for_input: str
        """

        self._pattern_for_input = pattern_for_input

    @property
    def prop_group_name(self):
        """Gets the prop_group_name of this PropertyDefinition.


        :return: The prop_group_name of this PropertyDefinition.
        :rtype: List[str]
        """
        return self._prop_group_name

    @prop_group_name.setter
    def prop_group_name(self, prop_group_name):
        """Sets the prop_group_name of this PropertyDefinition.


        :param prop_group_name: The prop_group_name of this PropertyDefinition.
        :type prop_group_name: List[str]
        """

        self._prop_group_name = prop_group_name

    @property
    def derivation(self):
        """Gets the derivation of this PropertyDefinition.

        属性の値が参照時に計算式によって計算される - 属性の値は編集不可能である - 伝播プロビジョニングによって、他の更新から伝播してマスタデータベースに値が保存される場合を除いて、データベースに値が保存されていない - 導出式が設定されている属性をキーにしたソートおよび検索はできない - 導出式が設定されている属性をパーティションの分割キーに指定することはできない  # noqa: E501

        :return: The derivation of this PropertyDefinition.
        :rtype: str
        """
        return self._derivation

    @derivation.setter
    def derivation(self, derivation):
        """Sets the derivation of this PropertyDefinition.

        属性の値が参照時に計算式によって計算される - 属性の値は編集不可能である - 伝播プロビジョニングによって、他の更新から伝播してマスタデータベースに値が保存される場合を除いて、データベースに値が保存されていない - 導出式が設定されている属性をキーにしたソートおよび検索はできない - 導出式が設定されている属性をパーティションの分割キーに指定することはできない  # noqa: E501

        :param derivation: The derivation of this PropertyDefinition.
        :type derivation: str
        """

        self._derivation = derivation

    @property
    def propagations(self):
        """Gets the propagations of this PropertyDefinition.


        :return: The propagations of this PropertyDefinition.
        :rtype: List[PropagationSetting]
        """
        return self._propagations

    @propagations.setter
    def propagations(self, propagations):
        """Sets the propagations of this PropertyDefinition.


        :param propagations: The propagations of this PropertyDefinition.
        :type propagations: List[PropagationSetting]
        """

        self._propagations = propagations

    @property
    def encryption(self):
        """Gets the encryption of this PropertyDefinition.

        属性を暗号化する場合に、その方式を設定する。  # noqa: E501

        :return: The encryption of this PropertyDefinition.
        :rtype: str
        """
        return self._encryption

    @encryption.setter
    def encryption(self, encryption):
        """Sets the encryption of this PropertyDefinition.

        属性を暗号化する場合に、その方式を設定する。  # noqa: E501

        :param encryption: The encryption of this PropertyDefinition.
        :type encryption: str
        """
        allowed_values = ["SSHA", "AES"]  # noqa: E501
        if encryption not in allowed_values:
            raise ValueError(
                "Invalid value for `encryption` ({0}), must be one of {1}"
                .format(encryption, allowed_values)
            )

        self._encryption = encryption

    @property
    def output_ldap_schema(self):
        """Gets the output_ldap_schema of this PropertyDefinition.

        OpenLDAP へのプロビジョニングで、この属性のスキーマを生成するかいなかを表すフラグ。 ただし、データ型がオブジェクトである場合は指定できず、スキーマを生成しない。  # noqa: E501

        :return: The output_ldap_schema of this PropertyDefinition.
        :rtype: bool
        """
        return self._output_ldap_schema

    @output_ldap_schema.setter
    def output_ldap_schema(self, output_ldap_schema):
        """Sets the output_ldap_schema of this PropertyDefinition.

        OpenLDAP へのプロビジョニングで、この属性のスキーマを生成するかいなかを表すフラグ。 ただし、データ型がオブジェクトである場合は指定できず、スキーマを生成しない。  # noqa: E501

        :param output_ldap_schema: The output_ldap_schema of this PropertyDefinition.
        :type output_ldap_schema: bool
        """

        self._output_ldap_schema = output_ldap_schema
