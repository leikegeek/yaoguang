#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/6/4 11:11 下午
# @Author : 竹芒
# @Version：V 0.1
# @File : db.py
# @desc :
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_caching import Cache

db = SQLAlchemy()
migrate = Migrate()
redis_cli = FlaskRedis()
cache = Cache()