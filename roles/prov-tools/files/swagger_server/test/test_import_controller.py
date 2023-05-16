# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.result import Result  # noqa: E501
from swagger_server.models.spool_list import SpoolList  # noqa: E501
from swagger_server.test import BaseTestCase


class TestImportController(BaseTestCase):
    """ImportController integration test stubs"""

    def test_import_file(self):
        """Test case for import_file

        ファイルをインポートする
        """
        query_string = [('action', 'action_example')]
        headers = [('http_remoteuser', 'http_remoteuser_example'),
                   ('http_remotegroup', 'http_remotegroup_example')]
        response = self.client.open(
            '/staff-importer/v1//spool/{name}'.format(name='name_example'),
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_spool(self):
        """Test case for list_spool

        ファイルの一覧を取得する
        """
        headers = [('http_remoteuser', 'http_remoteuser_example'),
                   ('http_remotegroup', 'http_remotegroup_example')]
        response = self.client.open(
            '/staff-importer/v1//spool',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
