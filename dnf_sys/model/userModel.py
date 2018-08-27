# -*- coding: utf-8 -*-
import bcrypt
import datetime
from dnf_sys import db
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    passhash = db.Column(db.String(128))
    active = db.Column(db.Boolean, default=True)
    authenticated = db.Column(db.Boolean, default=False)
    detail = db.relationship('UserDetailModel', backref='user_model', lazy='dynamic')
    authenticated = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    dt_create = db.Column(db.DateTime, default=datetime.datetime.now)
    dt_update = db.Column(db.DateTime, default=datetime.datetime.now)

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return self.authenticated

    @property
    def is_anonymous(self):
        return False

    @classmethod
    def register(cls, username, password,
                 is_active=True,
                 is_authenticated=True,
                 lvl=1):
        try:
            passhash = bcrypt.hashpw(password.encode('utf-8'),
                                     bcrypt.gensalt())
            user = cls(username=username,
                       passhash=passhash,
                       active=is_active,
                       authenticated=is_authenticated)
            db.session.add(user)
            db.session.commit()

            user_detail = UserDetailModel(user_id=user.id, lvl=lvl)
            db.session.add(user_detail)
            db.session.commit()
            ret = {
                'errcode': 0,
                'errmsg': 'OK',
                'data': user,
            }
        except Exception as e:
            db.session.rollback()
            ret = {
                'errcode': 500,
                'errmsg': e,
            }
        return ret

    @classmethod
    def login(cls, username, password):
        try:
            user = cls.query.filter_by(username=username).one()
            db.session.commit()
            if user.passhash.encode('utf-8') == bcrypt.hashpw(password.encode('utf-8'), user.passhash.encode('utf-8')):
                ret = {
                    'errcode': 0,
                    'errmsg': 'OK',
                    'data': user,
                }
            else:
                ret = {
                    'errcode': 1,
                    'errmsg': '密码输入错误,请重新输入',
                }
        except NoResultFound as e:
            db.session.rollback()
            ret = {
                'errcode': 2,
                'errmsg': '此用户不存在'
            }
        except MultipleResultsFound as e:
            db.session.rollback()
            ret = {
                'errcode': 3,
                'errmsg': 'duplicated user found, please check database'
            }
        except Exception as e:
            db.session.rollback()
            ret = {
                'errcode': 500,
                'errmsg': e,
            }
        return ret


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


