# -*- coding: utf-8 -*-
from flask import request, render_template, jsonify, flash, redirect
from flask_login import login_required, current_user
from dnf_sys import db, app, cfg
from dnf_sys.model.sysModel import LvlValidTimeModel, OrderModel, StoreHouseModel
from dnf_sys.helper import *


@app.route('/order_valid_time', methods=['GET', 'POST'])
@login_required
def orderValidTimeSet():
    if request.method == 'POST':
        valid_time = request.form.get("valid_time", "")
        user_lvl = request.form.get("user_lvl", "")
        try:
            # 单位为分钟
            valid_time = int(valid_time)
            user_lvl = int(user_lvl)
        except Exception as e:
            return render_template('error.html', error=e)
        if user_lvl not in [1,2,3]:
            ret = {
                "errcode": 3,
                "errmsg": "账号等级异常"
            }
            return jsonify(ret)
        m_lvl_valid = LvlValidTimeModel.query.filter_by(lvl=user_lvl)
        if not m_lvl_valid:
            lvl_valid = LvlValidTimeModel(
                lvl=user_lvl,
                valid_time=valid_time
            )
            db.session.add(lvl_valid)
        else:
            m_lvl_valid.valid_time = valid_time
        flash(message='设置成功', category='success')
        db.session.commit()
        return render_template('index.html', user=current_user)
    return render_template('order_valid_time.html', user=current_user)


@app.route('/order/new', methods=['GET', 'POST'])
@login_required
def order_new():
    if request.method == 'POST':
        # 订单有效时间(单位:分钟)
        try:
            valid_time = int(request.form.get("valid_time", ""))
            store_id = int(request.form.get("store_id", ""))
            gmoney = int(request.form.get("gmoney", ""))
            money = int(request.form.get("money", ""))
        except Exception as e:
            return jsonify({'errcode': 2, 'errmsg': u'请输入合理的订单信息'})
        user_id = current_user.id
        # 根据用户等级获取订单最大有效时长
        max_valid_time = get_valid_time_by_user_id(user_id)
        # 检测仓位是否被占用
        store_used = valid_store_is_used(store_id)
        if store_used:
            return jsonify({'errcode': 2, 'errmsg': u'sorry,仓位{}已经被占用！'.format(store_id)})
        if money % 10 != 0:
            return jsonify({'errcode': 3, 'errmsg': u'金钱数必须为10的整数倍，谢谢配合！'.format(int(max_valid_time))})
        if valid_time > int(max_valid_time):
            return jsonify({'errcode': 3, 'errmsg': u'您目前订单最大有效时长为{}分钟, 敬请谅解！'.format(int(max_valid_time))})
        m_order = OrderModel(
            store_id=store_id,
            user_id=user_id,
            money=money,
            gmoney=gmoney,
            valid_time=valid_time,
            status='wait_pay'
        )
        db.session.add(m_order)
        # 更新仓位状态为被占用
        StoreHouseModel.query.get(int(store_id)).is_used = True
        db.session.commit()
        return redirect('/order/list')
    return redirect('/order/list')


@app.route('/order/list', methods=['GET', 'POST'])
@login_required
def order_list():
    page_num = int(request.args.get('page_num', 1))
    page_size = int(request.args.get('page_size', 20))
    # 为管理员查询某个人订单做预留
    if request.args.get('user_id', ''):
        user_id = int(request.args.get('user_id'))
    else:
        user_id = current_user.id
    if is_manager(user_id):
        m_order = OrderModel.query.offset((page_num - 1) * page_size).limit(page_size).all()
    else:
        m_order = OrderModel.query.filter_by(user_id=user_id) \
                            .offset((page_num - 1) * page_size) \
                            .limit(page_size) \
                            .all()
    rst = [i.to_dict() for i in m_order]
    return render_template('order_list.html', order_list=rst, user=current_user, area_list=get_area_list())


@app.route('/store/list', methods=['GET', 'POST'])
@login_required
def store_list():
    page_num = int(request.args.get('page_num', 1))
    page_size = int(request.args.get('page_size', 20))
    if request.args.get('user_id', ''):
        user_id = int(request.args.get('user_id'))
    else:
        user_id = current_user.id
    if is_manager(user_id):
        # 管理员
        m_store = StoreHouseModel.query.offset((page_num - 1) * page_size).limit(page_size).all()
        rst = [i.to_dict() for i in m_store]
        return render_template('order_list.html', store_list=rst, user=current_user)
    # 获取当前用户大区id
    m_larea = get_user_larea_id_by_user_id(user_id)
    m_store = StoreHouseModel.query.filter_by(area_id=m_larea['id']) \
                        .order_by(StoreHouseModel.store_id) \
                        .offset((page_num - 1) * page_size) \
                        .limit(page_size) \
                        .all()
    # 获取当前指导比例
    curr_sale_price = get_recent_price(datetime.datetime.now(), m_larea['id'])
    rst = [i.to_dict() for i in m_store]
    return render_template('order_list.html', order_list=rst, user=current_user, curr_sale_price=curr_sale_price)
