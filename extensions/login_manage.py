#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/6/6 11:37 上午
# @Author : 竹芒
# @Version：V 0.1
# @File : login_manage.py
# @desc : 登录管理类
import base64
import hashlib
import os
import time

from flask import current_app, request, session
from flask_login import LoginManager, login_user, logout_user
from flask_restful import marshal, fields
from .db import cache


class CustomLoginManager(LoginManager):
    def __init__(self, app=None, add_context_processor=True, message=None):
        super(CustomLoginManager, self).__init__(
            app=app, add_context_processor=add_context_processor)

        self.err_message = message


login_manager = CustomLoginManager()
login_item = {
    'url': fields.String(default=''),
    'message': fields.String(default='')
}
REDIS_KEY_NONCE = 'YG:APINONCE:%s'
NONCE_EXPIRE = 30


