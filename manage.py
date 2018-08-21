# -*- coding: utf-8 -*-

from dnf_sys import db, app
from flask_script import Manager, prompt_bool, Server
from dnf_sys.model import userModel, sysModel

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


manager.add_command('runserver',Server(host='0.0.0.0', port=8888))

@manager.shell
def make_shell_context():
    return dict(app=app,db=db)


if __name__ == "__main__":
    manager.run()
