# -*- coding: utf-8 -*-
import datetime
from flask import request, render_template, jsonify, redirect, flash
from flask_login import login_required, current_user
from dnf_sys import db, app
from dnf_sys.model.sysModel import SalePriceModel, AreaModel
from sqlalchemy import desc, and_


@app.route('/saleprice/new', methods=['GET', 'POST'])
@login_required
def salePrice_new():
    tkn = request.args.get('jwt', '')
    if request.method == 'POST':
        valid_time = request.form.get("valid_time", "")
        price = request.form.get("sale_price", "")
        area_name = request.form.get("area_name", "")
        m_area = AreaModel.query.filter(and_(AreaModel.area_name == area_name, AreaModel.parent_id == 0)).one_or_none()
        if not m_area:
            return jsonify({'errmsg':'大区获取错误'})
        try:
            valid_time = datetime.datetime.strptime(valid_time, '%Y-%m-%d %H:%M')
            price = int(price)
        except Exception as e:
            return render_template('error.html', error=e)
        new_sale_price = SalePriceModel(
            sale_price=price,
            valid_time=valid_time,
            area_id=m_area.id
        )
        db.session.add(new_sale_price)
        db.session.commit()
        flash('新建成功', 'success')
        return redirect('/index')
    return render_template('sale_price.html', tkn=tkn)


def salePrice_list(area):
    m_area = AreaModel.query.filter(and_(AreaModel.area_name == area, AreaModel.parent_id == 0)).one_or_none()
    if not m_area:
        return jsonify({'errmsg':'大区获取错误'})
    area_id = m_area.id
    now = datetime.datetime.now()
    date_early_one = now - datetime.timedelta(days=1)
    date_early_two = now - datetime.timedelta(days=2)
    date_early_three = now - datetime.timedelta(days=3)
    date_early_four = now - datetime.timedelta(days=4)
    date_early_five = now - datetime.timedelta(days=5)
    date_early_six = now - datetime.timedelta(days=6)
    date_early_seven = now - datetime.timedelta(days=7)

    ret = {
        "date_early_seven": {"source_data": date_early_seven, "rst":[]},
        "date_early_six": {"source_data": date_early_six, "rst":[]},
        "date_early_five": {"source_data": date_early_five, "rst":[]},
        "date_early_four": {"source_data": date_early_four, "rst":[]},
        "date_early_three": {"source_data": date_early_three, "rst":[]},
        "date_early_two": {"source_data": date_early_two, "rst":[]},
        "date_early_one": {"source_data": date_early_one, "rst":[]},
    }
    for item in ret:
        data_one = SalePriceModel.query.filter(and_(get_date_ret(ret[item]["source_data"])['two'] > SalePriceModel.valid_time,
            SalePriceModel.valid_time >= get_date_ret(ret[item]["source_data"])['one'], SalePriceModel.area_id == area_id))\
            .order_by(desc(SalePriceModel.valid_time)).all()
        data_two = SalePriceModel.query.filter(and_(get_date_ret(ret[item]["source_data"])['three'] > SalePriceModel.valid_time,
            SalePriceModel.valid_time >= get_date_ret(ret[item]["source_data"])['two'], SalePriceModel.area_id == area_id))\
            .order_by(desc(SalePriceModel.valid_time)).all()
        data_three = SalePriceModel.query.filter(and_(get_date_ret(ret[item]["source_data"])['four'] > SalePriceModel.valid_time,
            SalePriceModel.valid_time >= get_date_ret(ret[item]["source_data"])['three'], SalePriceModel.area_id == area_id))\
            .order_by(desc(SalePriceModel.valid_time)).all()
        data_four = SalePriceModel.query.filter(and_(get_date_ret(ret[item]["source_data"])['five'] > SalePriceModel.valid_time,
            SalePriceModel.valid_time >= get_date_ret(ret[item]["source_data"])['four'], SalePriceModel.area_id == area_id))\
            .order_by(desc(SalePriceModel.valid_time)).all()
        ret[item]["rst"].append(data_one[0].sale_price if data_one != [] else \
            get_recent_price(get_date_ret(ret[item]["source_data"])['one'], area_id))
        ret[item]["rst"].append(data_two[0].sale_price if data_two != [] else \
            get_recent_price(get_date_ret(ret[item]["source_data"])['two'], area_id))
        ret[item]["rst"].append(data_three[0].sale_price if data_three != [] else \
            get_recent_price(get_date_ret(ret[item]["source_data"])['three'], area_id))
        ret[item]["rst"].append(data_four[0].sale_price if data_four != [] else \
            get_recent_price(get_date_ret(ret[item]["source_data"])['four'], area_id))
    for i in ret:
        ret[i]["source_data"] = ret[i]["source_data"].strftime( "%Y-%m-%d")
    return ret


def get_recent_price(date, area_id):
    m_list = SalePriceModel.query.filter(and_(SalePriceModel.area_id == area_id,
        SalePriceModel.valid_time < date)).order_by(desc(SalePriceModel.valid_time)).all()
    if m_list:
        return m_list[0].sale_price
    else:
        return 0


def get_date_ret(date):
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    now_one = year + '-' + month + '-' + day + ' ' + '00:00:00'
    now_two = year + '-' + month + '-' + day + ' ' + '06:00:00'
    now_three = year + '-' + month + '-' + day + ' ' + '12:00:00'
    now_four = year + '-' + month + '-' + day + ' ' + '18:00:00'
    now_five = year + '-' + month + '-' + day + ' ' + '23:59:59'
    return {
        'one': str2dt(now_one),
        'two': str2dt(now_two),
        'three': str2dt(now_three),
        'four': str2dt(now_four),
        'five': str2dt(now_five),
    }

def str2dt(my_str):
    return datetime.datetime.strptime(my_str, '%Y-%m-%d %H:%M:%S')
