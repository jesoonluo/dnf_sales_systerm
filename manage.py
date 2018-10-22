# -*- coding: utf-8 -*-

import datetime
from dnf_sys import db, app
from flask_script import Manager, prompt_bool, Server
from dnf_sys.model import userModel, sysModel
from dnf_sys.sale_price import str2dt

manager = Manager(app)

@manager.command
def initdb():
    if prompt_bool("Are you sure? You will init your database"):
        db.create_all()


@manager.command
def dropdb():
    if prompt_bool("Are you sure? You will lose all your data!"):
        db.drop_all()


@manager.command
def init_data():
    area_dict = {
        '跨一': [
            '广东1区', '广东2区', '广东3区', '广东4区', '广东5区', '广东6区','广东7区', '广东8区', '广东9区',
            '广东10区', '广东11区', '广东12区', '广东13区', '广州1/2区', '广西1区', '广西2/4区', '广西3区', '广西5区',
        ],
        '跨二': [
            '湖北1区', '湖北2区', '湖北3区', '湖北4区', '湖北5区', '湖北6区', '湖北7区', '湖北8区',
            '湖南1区', '湖南2区', '湖南3区', '湖南4区', '湖南5区', '湖南6区', '湖南7区'
        ],
        '跨三A':[
            '四川1区', '四川2区', '四川3区', '四川4区', '四川5区', '四川6区',
            '西北1区', '西北2/3区', '新疆1区',
        ],
        '跨三B':[
            '贵州1区', '陕西1区', '陕西2/3区', '西南1区', '西南2区', '西南3区', '云贵1区',
            '云南1区', '重庆1区', '重庆2区',
        ],
        '跨四':[
            '安徽3区', '福建3/4区', '江苏5/7区', '江苏6区', '江苏8区', '江西3区',
            '上海4/5区', '浙江4/5区', '浙江6区', '浙江7区',
        ],
        '跨五':[
            '安徽1区', '安徽2区', '福建1区', '福建2区', '江苏1区', '江苏2区', '江苏3区', '江苏4区',
            '江西1区', '江西2区', '上海1区', '上海2区', '上海3区', '浙江1区', '浙江2区', '浙江3区',
        ],
        '跨六':[
            '北京1区', '北京2/4区', '东北1区', '东北2区','东北3/7区', '河北1区', '河南1区', '河南2区', '黑龙江1区',
            '华北1区', '华北2区', '华北3区', '吉林1/2区', '辽宁1区', '山东1区', '山东2/7区', '山西1区',
        ],
        '跨七':[
            '辽宁2区', '辽宁3区', '东北4/5/6区', '河北2/3区', '河北4区', '河北5区',
            '河南3区', '河南4区', '河南5区', '河南6区', '河南7区',
        ],
        '跨八':[
            '山西2区', '黑龙江2/3区', '北京3区', '天津1区', '内蒙古1区', '华北4区', '山东3区',
            '山东4区', '山东5区', '山东6区',
        ],
    }
    # 初始化areamodel
    for lg_area in area_dict:
        area_large = sysModel.AreaModel(
            parent_id=0,
            area_name=lg_area
        )
        db.session.add(area_large)
    db.session.commit()
    # 创建对应的仓位号
    for area_large in range(1,10):
        range_list = ['{0:03}'.format(item) for item in range(1,1000)]
        for i in range_list:
            store = sysModel.StoreHouseModel(
                area_id=area_large,
                store_id=str(area_large) + str(i)
            )
            db.session.add(store)
        db.session.commit()
        # 创建跨区下子分区
        lg_area_name = sysModel.AreaModel.query.get(area_large).area_name
        print('start_init:', lg_area_name)
        for md_area in area_dict[lg_area_name]:
            area_middle = sysModel.AreaModel(
                parent_id=area_large,
                area_name=md_area
            )
            db.session.add(area_middle)
        db.session.commit()
    # 大区指导比例初始化
    now = datetime.datetime.now()
    date_early_one = now - datetime.timedelta(days=1)
    date_early_two = now - datetime.timedelta(days=2)
    date_early_three = now - datetime.timedelta(days=3)
    date_early_four = now - datetime.timedelta(days=4)
    date_early_five = now - datetime.timedelta(days=5)
    date_early_six = now - datetime.timedelta(days=6)
    date_early_seven = now - datetime.timedelta(days=7)
    ret = {
        "date_early_seven": date_early_seven,
        "date_early_six": date_early_six,
        "date_early_five": date_early_five,
        "date_early_four": date_early_four,
        "date_early_three": date_early_three,
        "date_early_two": date_early_two,
        "date_early_one": date_early_one,
    }
    for item in ret:
        year = str(ret[item].year)
        month = str(ret[item].month)
        day = str(ret[item].day)
        now_one = str2dt(year + '-' + month + '-' + day + ' ' + '00:10:00')
        for i in range(1,10):
            m_sp = sysModel.SalePriceModel(
                area_id=i,
                sale_price=40,
                valid_time=now_one
            )
            db.session.add(m_sp)
        now_two = str2dt(year + '-' + month + '-' + day + ' ' + '06:10:00')
        for i in range(1,10):
            m_sp = sysModel.SalePriceModel(
                area_id=i,
                sale_price=50,
                valid_time=now_two
            )
            db.session.add(m_sp)
        now_three = str2dt(year + '-' + month + '-' + day + ' ' + '12:10:00')
        for i in range(1,10):
            m_sp = sysModel.SalePriceModel(
                area_id=i,
                sale_price=60,
                valid_time=now_three
            )
            db.session.add(m_sp)
        now_four = str2dt(year + '-' + month + '-' + day + ' ' + '18:10:00')
        for i in range(1,10):
            m_sp = sysModel.SalePriceModel(
                area_id=i,
                sale_price=70,
                valid_time=now_four
            )
            db.session.add(m_sp)
    db.session.commit()
    print('指导比例初始化成功')
    # 用户注册
    user = userModel.UserModel.register(
        username='liqi',
        password='123456',
        area_id=0,  # 管理员
        lvl=3
    )
    user = userModel.UserModel.register(
        username='test',
        password='123456',
        area_id=44  # 普通用户
    )
    # 设置用户等级有效时长(单位:分)
    user_lvl_to_valid_time = {
        '1': 100,
        '2': 200,
        '3': 600
    }
    for user_lvl in range(1,4):
        lvl_valid = sysModel.LvlValidTimeModel(
            lvl=user_lvl,
            valid_time=int(user_lvl_to_valid_time[str(user_lvl)])
        )
        db.session.add(lvl_valid)
    db.session.commit()
    print('用户等级有效时长设置成功,一级100分钟,二级200分钟,三级600分钟')
    if user['errcode'] == 0:
        print ('初始化用户成功')
    else:
        print ('初始化用户失败')
        print(user['errmsg'])


manager.add_command('runserver',Server(host='0.0.0.0', port=8888))

@manager.shell
def make_shell_context():
    return dict(app=app,db=db)


if __name__ == "__main__":
    manager.run()
