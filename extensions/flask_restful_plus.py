#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/6/2 11:21 下午
# @Author : 竹芒
# @Version：V 0.1
# @File : flask_restful_plus.py
# @desc : flask_restful 增强
import flask.json
from flask import current_app
from flask_babel import gettext
from flask_restful.reqparse import Argument
import flask_restful
import six


class CustomArgument(Argument):
    """自定义参数处理类"""
    def handle_validation_error(self, error, bundle_errors):
        error_str = six.text_type(error)
        error_msg = self.help.format(error_msg=error_str) if self.help else error_str
        msg = {self.name: error_msg}
        if current_app.config.get("bundle_errors", False) or bundle_errors:
            return error, msg
        error_dct = [{
            'code': 400,
            'message': error_str,
            'details': {
               'field': self.name,
               'error': repr(error)
            }
        }]
        current_app.logger.warning(f'ArgumentError:{error_dct}')
        flask_restful.abort(400, message=(f"{gettext('ArgumentError')}'{self.name}': "
                            f'{gettext(error_str)}'),errors=error_dct)


class TimestampField(flask_restful.fields.Raw):
    def format(self, value):
        return int(value.timestamp() * 1000)


