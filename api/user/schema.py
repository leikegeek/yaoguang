#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/6/2 11:24 下午
# @Author : 竹芒
# @Version：V 0.1
# @File : schema.py
# @desc :

from extensions.flask_restful_plus import CustomArgument, TimestampField
from flask_restful import fields, reqparse, inputs
from model.user import User, Role
import extensions


def validate_role(role_id, name, *args):
    extensions.Assert(Role.get_by_id(role_id) is not None, ValueError(f'tips.role.not.exists'))
    return int(role_id)


user_item = {
    'id': fields.String,
    'username': fields.String,
    'role_name': fields.String,
    'role_id': fields.Integer,
    'create_by': fields.String,
    'create_dt': TimestampField
}

user_list_item = {
    'total': fields.Integer,
    'items': fields.String
}

list_parse = reqparse.RequestParser(argument_class=CustomArgument, trim=True)

