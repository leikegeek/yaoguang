#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/6/5 7:54 下午
# @Author : 竹芒
# @Version：V 0.1
# @File : babel.py
# @desc :
from flask import request
from flask_babel import Babel

DEFAULT_LOCAL = 'zh'
LOCALE_CHOICE = ['en', DEFAULT_LOCAL]
babel = Babel(default_locale=DEFAULT_LOCAL)


@babel.localeselector
def get_local():
    return request.accept_languages.best_match(LOCALE_CHOICE) or DEFAULT_LOCAL


@babel.timezoneselector
def get_timezone():
    return
