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

from flask import current_app, request, session, redirect
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


@login_manager.unauthorized_handler
def unauthorized():
    current_app.logger.info(' not login')
    if(
        request.headers.get('X-Requested-With') == 'XMLHttpRequest' or
        login_manager.err_message
    ):
        if login_manager.err_message:
            return marshal({'message': login_manager.err_message}, login_item), 400
        return marshal({'url': 'https://login'}, login_item), 401

    return redirect('https://login')


@login_manager.request_loader
def request_loader(req):
    auth_header = req.headers.get('Authorization')
    if not auth_header:
        return
    current_app.logger.info(f'Request Headers:{req.headers}')
    try:
        timestamp = req.headers.get('X-YG-Time')
        nonce = req.headers.get('X-YG-Nonce')
        key = REDIS_KEY_NONCE % nonce
        _, auth_str = auth_header.split()
        app_id, signature = base64.b64decode(auth_str).decode().split(':')
