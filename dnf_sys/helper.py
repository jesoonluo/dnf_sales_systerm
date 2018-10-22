# -*- coding: utf-8 -*-
import datetime
from dnf_sys.model.sysModel import LvlValidTimeModel, SalePriceModel, AreaModel, StoreHouseModel
from dnf_sys.model.userModel import UserDetailModel
from sqlalchemy import desc, and_

def str2dt(my_str):
    return datetime.datetime.strptime(my_str, '%Y-%m-%d %H:%M:%S')


def get_valid_time_by_user_id(user_id):
    m_user = UserDetailModel.query.filter_by(user_id=int(user_id)).one_or_none()
    if m_user:
        m_lvl = LvlValidTimeModel.query.filter_by(lvl=m_user.lvl).one_or_none()
        if m_lvl:
            return m_lvl.valid_time
    return False

def is_manager(user_id):
    m_user = UserDetailModel.query.filter_by(user_id=int(user_id)).one_or_none()
    if m_user:
        if int(m_user.area_id) == 0:
            return True
    return False

def get_recent_price(date, area_id):
    m_list = SalePriceModel.query.filter(and_(SalePriceModel.area_id == area_id,
        SalePriceModel.valid_time < date)).order_by(desc(SalePriceModel.valid_time)).all()
    if m_list:
        return m_list[0].sale_price
    else:
        return 0

def get_area_by_user_id(user_id):
    m_user = UserDetailModel.query.filter_by(user_id=int(user_id)).one_or_none()
    if m_user:
        # 管理员
        if m_user.area_id == 0:
            return jsonify({'errcode': 1, 'errmsg': '此用户为管理员'})
        m_area = AreaModel.query.get(m_user.area_id).one_or_none()
    if m_area:
        return m_area.to_dict()
    return jsonify({'errcode': 1, 'errmsg': '用户不存在'})

def get_user_larea_id_by_user_id(user_id):
    '''获取用户大区id'''
    m_user = UserDetailModel.query.filter_by(user_id=int(user_id)).one_or_none()
    if m_user:
        # 管理员
        if m_user.area_id == 0:
            return {'errcode': 1, 'errmsg': '此用户为管理员'}
        m_area = AreaModel.query.get(m_user.area_id)
    if m_area:
        m_larea = AreaModel.query.get(m_area.parent_id)
        return m_larea.to_dict()
    return None

def valid_store_is_used(store_id):
    m_store = StoreHouseModel.query.get(store_id)
    return m_store.is_used

def get_area_list():
    m_area_list = AreaModel.query.filter_by(parent_id=0).all()
    area_name_list = [i.area_name for i in m_area_list]
    return area_name_list
