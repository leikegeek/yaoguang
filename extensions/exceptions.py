#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/6/10 11:37 下午
# @Author : 竹芒
# @Version：V 0.1
# @File : exceptions.py
# @desc : 异常处理类

from dataclasses import dataclass, field

@dataclass
class YgExceptions(Exception):
    code: int = 5000
    detail: dict = field(default_factory=dict)
    message: str = ''

    def __str__(self):
        return f'{self.message}'

    def get_details(self):
        return self.detail

    def get_message(self):
        return self.message or str(self)


class APIException(YgExceptions):
    pass


@dataclass
class NullException(APIException):
    code:int = 1000


@dataclass
class DuplicationException(APIException):
    code: int = 1001
    identify: str = ''

    def get_details(self):
        return {'set_name': self.identify}

    def get_message(self):
        return f'{self.identify} already exists'

@dataclass
class BadArguments(APIException):
    code: int = 2000


@dataclass
class AuthorizationError(APIException):
    code: int = 2001

