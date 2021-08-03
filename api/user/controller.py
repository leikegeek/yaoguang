#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/6/2 10:51 下午
# @Author : 竹芒
# @Version：V 0.1
# @File : controller.py
# @desc :用户模块controller
from flask import Blueprint, make_response
from flask_login import login_required
from flask_restful import Api, Resource, marshal
from model.user import User
from api.user.schema import list_parser, add_parser

bp = Blueprint('user', __name__, url_prefix='/api/user')
api = Api(bp)


@bp.before_request
@login_required
def before_request():
    """请求预处理"""
    ...

class User(Resource):
    def post(self):
        data = add_parser.parse_args(strict=True)


api.add_resource(User, '')

