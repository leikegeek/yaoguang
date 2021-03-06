#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/6/1 11:04 下午
# @Author : 竹芒
# @Version：V 0.1
# @File : user.py
# @desc :
from flask_login import UserMixin, current_user
from sqlalchemy import Boolean, Column, Integer, String, Text, or_
from .base import BaseModel
from .role import Role
from .role_menu import RoleMenu
from extensions.db import cache
from extensions import exceptions

class User(BaseModel):
    __tablename__ = 'user'
    username = Column(String(100), nullable=False)

    @classmethod
    def filter_by_criteria(cls, query, criteria):
        if criteria.get('keywords'):
            query = query.filter(cls.username.contains(criteria['keywords']))
        return query

    @classmethod
    def create(cls, username):
        exceptions.Assert(not cls.exists(username), exceptions.DuplicationException(identify=username))
        return super.create(username=username)

    @classmethod
    def exists(cls, username):
        return cls.get_by_id(username) is not None

    @classmethod
    def get_by_id(cls, username, create_ne=False):
        user = cls.dq().filter(cls.username == username).first()
        if user:
            return user
        if create_ne:
            return cls.create(username=username)


