# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from task_executer.models.base_model_ import Model
from task_executer import util


class ResponseBody(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, result=None, failed_data=None):  # noqa: E501
        """ResponseBody - a model defined in OpenAPI

        :param result: The result of this ResponseBody.  # noqa: E501
        :type result: str
        :param failed_data: The failed_data of this ResponseBody.  # noqa: E501
        :type failed_data: str
        """
        self.openapi_types = {
            'result': str,
            'failed_data': str
        }

        self.attribute_map = {
            'result': 'result',
            'failed_data': 'failedData'
        }

        self._result = result
        self._failed_data = failed_data

    @classmethod
    def from_dict(cls, dikt) -> 'ResponseBody':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The responseBody of this ResponseBody.  # noqa: E501
        :rtype: ResponseBody
        """
        return util.deserialize_model(dikt, cls)

    @property
    def result(self):
        """Gets the result of this ResponseBody.


        :return: The result of this ResponseBody.
        :rtype: str
        """
        return self._result

    @result.setter
    def result(self, result):
        """Sets the result of this ResponseBody.


        :param result: The result of this ResponseBody.
        :type result: str
        """
        allowed_values = ["completed", "failed"]  # noqa: E501
        if result not in allowed_values:
            raise ValueError(
                "Invalid value for `result` ({0}), must be one of {1}"
                .format(result, allowed_values)
            )

        self._result = result

    @property
    def failed_data(self):
        """Gets the failed_data of this ResponseBody.


        :return: The failed_data of this ResponseBody.
        :rtype: str
        """
        return self._failed_data

    @failed_data.setter
    def failed_data(self, failed_data):
        """Sets the failed_data of this ResponseBody.


        :param failed_data: The failed_data of this ResponseBody.
        :type failed_data: str
        """

        self._failed_data = failed_data
