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


class OrderModel(db.Model):
    '''订单表'''
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer)  # 仓位id
    area_name = db.Column(db.String(64), unique=True)
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


class SalePriceModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_price = db.Column(db.Integer)
    is_deleted = db.Column(db.Boolean, default=False)
    valid_time = db.Column(db.DateTime, default=datetime.datetime.now)
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
