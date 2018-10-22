# -*- coding: utf-8 -*-
from dnf_sys import db
import datetime


class AreaModel(db.Model):
    '''大区表'''
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer)
    area_name = db.Column(db.String(64), unique=True)
    is_deleted = db.Column(db.Boolean, default=False)
    dt_create = db.Column(db.DateTime, default=datetime.datetime.now)
    dt_update = db.Column(db.DateTime, default=datetime.datetime.now)

    def to_dict(self):
        ret_dict = {}
        for k in self.__table__.columns:
            value = getattr(self, k.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d')
            ret_dict[k.name] = value if value else ''
        return ret_dict


class OrderModel(db.Model):
    '''订单表'''
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer)    # 仓位id
    user_id = db.Column(db.Integer)     # 用户id
    valid_time = db.Column(db.Integer)  # 订单有效时间
    status = db.Column(db.String(32))   # 订单状态
    gmoney = db.Column(db.Integer)      # 游戏币
    money = db.Column(db.Integer)       # 人民币
    is_deleted = db.Column(db.Boolean, default=False)
    dt_create = db.Column(db.DateTime, default=datetime.datetime.now)
    dt_update = db.Column(db.DateTime, default=datetime.datetime.now)

    def to_dict(self):
        ret_dict = {}
        for k in self.__table__.columns:
            value = getattr(self, k.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d')
            ret_dict[k.name] = value if value else ''
        return ret_dict


class LvlValidTimeModel(db.Model):
    '''账号等级与订单有效时间对应表'''
    id = db.Column(db.Integer, primary_key=True)
    lvl = db.Column(db.Integer)
    valid_time = db.Column(db.Integer)  # 有效时间,单位(分)
    is_deleted = db.Column(db.Boolean, default=False)
    dt_create = db.Column(db.DateTime, default=datetime.datetime.now)
    dt_update = db.Column(db.DateTime, default=datetime.datetime.now)


class StoreHouseModel(db.Model):
    '''仓库表'''
    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer)    # 大区id
    store_id = db.Column(db.String(16))   # 仓位号
    is_used = db.Column(db.Boolean, default=False)  # 是否使用中
    is_deleted = db.Column(db.Boolean, default=False)
    dt_create = db.Column(db.DateTime, default=datetime.datetime.now)
    dt_update = db.Column(db.DateTime, default=datetime.datetime.now)

    def to_dict(self):
        ret_dict = {}
        for k in self.__table__.columns:
            value = getattr(self, k.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d')
            ret_dict[k.name] = value if value else ''
        return ret_dict


class SalePriceModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer)    # 大区id
    sale_price = db.Column(db.Integer)
    valid_time = db.Column(db.DateTime, default=datetime.datetime.now)
    is_deleted = db.Column(db.Boolean, default=False)
    dt_create = db.Column(db.DateTime, default=datetime.datetime.now)
    dt_update = db.Column(db.DateTime, default=datetime.datetime.now)

    def to_dict(self):
        ret_dict = {}
        for k in self.__table__.columns:
            value = getattr(self, k.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d')
            ret_dict[k.name] = value if value else ''
        return ret_dict
