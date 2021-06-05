#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/6/1 11:05 下午
# @Author : 竹芒
# @Version：V 0.1
# @File : base.py
# @desc :
from datetime import datetime
from flask_login import current_user
from sqlalchemy import inspect
from sqlalchemy import Boolean, Column, Integer, DateTime, String
from extensions.db import db, cache
from .constant import(
     DEFAULT_PAGE,
     DEFAULT_PAGE_CAP,
     MAX_PAGE_CAP,
     REDIS_KEY_ITEM_BY_ID,
     REDIS_KEY_ITEM_BY_ID_FOR_SHARE
)



def get_current_user():
    return current_user.get_id() or 'anonymous'


class Base(db.Model):
    __abstract__ = True
    """默认审计字段"""
    create_at = Column(DateTime, default=datetime.now, nullable=False)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now(), nullable=False)
    create_by = Column(String, nullable=False, default=get_current_user())
    update_by = Column(String, nullable=False, default=get_current_user())

    @classmethod
    def dq(cls, with_del=False):
        return cls.query

    @classmethod
    def order_by(cls, query):
        return query.order_by(-cls.create_at)

    @classmethod
    def filter_by_criteria(cls, query, criteria):
        return query

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        obj.session.add(obj)
        obj.sessoin.commit()
        cls.cache_obj(obj)
        return obj

    @classmethod
    def bulk_create(cls, objs):
        db.session.bulk_save_objects(objs)
        db.session.commit()

    @classmethod
    def get_all(cls, criteria: dict = None,
                with_page: bool = True,
                page: int = DEFAULT_PAGE,
                per_page: int = DEFAULT_PAGE_CAP):
        query = cls.filter_by_criteria(cls.dq(), criteria)
        query = cls.order_by(query)
        if with_page:
            return query.paginate(page, per_page, error_out=False, max_per_page=MAX_PAGE_CAP)
        return query

    def delete(self):
        f = db.session.delete(self)
        db.session.commit()
        self.flush_cache()
        return f

    @classmethod
    def flush_cache(cls, target):
        fmt_data = (target.__class__.__name__, target.id)
        cache.cache.delete_many(
            REDIS_KEY_ITEM_BY_ID % fmt_data,
            REDIS_KEY_ITEM_BY_ID_FOR_SHARE % fmt_data
        )
        target.clear_self_cache()

    @classmethod
    def cache_obj(cls, obj):
        pass

    def clear_self_cache(self):
        pass

    def to_dict(self):
        """convert model object to dict object"""
        return {
            c.key: getattr(self, c.key, None)
            for c in inspect(self).mapper.column_attrs
        }

    def resolve(self):
        return self.to_dict()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    is_del = Column(Boolean, default=False)

    @classmethod
    def dq(cls, with_del=False):
        query = cls.query
        if not with_del:
            query = query.filter(cls.is_del.is_(False))
        return query

    @classmethod
    def get_by_id(cls, obj_id, form_cache=True):
        if not form_cache:
            return cls.dq().filter(cls.id == obj_id).first()
        cache_key = REDIS_KEY_ITEM_BY_ID % (cls.__name__, obj_id)
        obj = cache.cache.get(cache_key)
        if not obj:
            obj = cls.dq().filter(cls.id == obj_id).first()
            if obj:
                obj.cache_obj(obj)
            return obj

    def update(self, **kwargs):
        column = inspect(self).mapper.column_attrs
        db.session.query(self.__class__).filter(self.__class__.id == self.id)\
            .update({
                k: v
                for k, v in kwargs.items()
                if hasattr(column, k) and getattr(self, k) != v
            })
        db.session.commit()
        self.flush_cache(self)
        return self.get_by_id(self.id)

    @classmethod
    def cache_obj(cls, obj):
        fmt_data = (cls.__name__, obj.id)
        cache_data = {
            REDIS_KEY_ITEM_BY_ID % fmt_data: obj,
            REDIS_KEY_ITEM_BY_ID_FOR_SHARE % fmt_data: obj.resolve()
        }
        cache.cache.set_many(cache_data, timeout=0)
