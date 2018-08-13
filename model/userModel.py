# -*- coding: utf-8 -*-
from db import db


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    passhash = db.Column(db.String(128))
    active = db.Column(db.Boolean, default=True)
    authenticated = db.Column(db.Boolean, default=False)
    detail = db.relationship('UserDetailModel', backref='user_model', lazy='dynamic')
    is_deleted = db.Column(db.Boolean, default=False)
    dt_create = db.Column(db.DateTime, default=datetime.datetime.now)
    dt_update = db.Column(db.DateTime, default=datetime.datetime.now)


class UserDetailModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lvl = db.Column(db.Integer)   # 账号权限等级
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    gender = db.Column(db.String(16))
    english_name = db.Column(db.String(32))
    chinese_name = db.Column(db.String(32),default='')
    avatar = db.Column(db.String(255),default='/static/pic/avatar.jpg')
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    wechat = db.Column(db.String(32))
    qq = db.Column(db.String(32))
    address = db.Column(db.String(255))
    extra = db.Column(db.String(255), default='')
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
