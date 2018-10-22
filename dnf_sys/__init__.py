# -*- coding: utf-8 -*-
import jwt
import datetime
from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template, redirect, request
from flask_login import LoginManager, login_required, current_user
from dnf_sys import cfg


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = cfg.DB_SERVER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_NAME'] = 'Ssession'
app.config['REMEMBER_COOKIE_DURATION'] = datetime.timedelta(hours=2)
app.config['TESTING'] = False
app.secret_key = cfg.secret_key
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

import dnf_sys.sale_price
import dnf_sys.user
import dnf_sys.order
from dnf_sys.model.userModel import UserModel
from dnf_sys.model.sysModel import AreaModel
from dnf_sys.sale_price import salePrice_list
from dnf_sys.helper import get_area_by_user_id, is_manager, get_area_list

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(user_id)

@login_manager.unauthorized_handler
def notLogin():
    return '请先登录'

def _verify_token(tkn):
    try:
        # 验证管理者登录的用户的JWT
        d = jwt.decode(tkn, cfg.mc_jwt)
        phone = d.get("phone", "")
        pwd = d.get("pwd", "")
        if not phone == "1234":
            return None, None, "无效的账号。"
        if not pwd == '1234':
            return None, None, "密码错误"
        return phone, pwd, ""
    except Exception as e:
        return None, None, str(e)

@app.route('/index')
@login_required
def index():
    if not is_manager(current_user.id):
        return u'请联系管理员获取权限'
    # 大区指导比例, 默认一区
    area = request.args.get('area', '跨一')
    sp_list = salePrice_list(area)
    date_range = []
    value = sp_list.values()
    line_data = [
        {"name":"时段一", "data":[]},
        {"name":"时段二", "data":[]},
        {"name":"时段三", "data":[]},
        {"name":"时段四", "data":[]},
    ]
    for item in value:
        date_range.append(item['source_data'])
        for i in range(4):
            line_data[i]["data"].append(item['rst'][i])
    area_name_list = get_area_list()
    return render_template(
        "index.html",
        user=current_user,
        line_data=line_data,
        date_range=date_range,
        area_list=area_name_list,
        area=area
    )


@app.route('/seller_index')
def seller_index():
    area = request.args.get('area', None)
    m_area_list = AreaModel.query.filter_by(parent_id=0).all()
    area_name_list = [i.area_name for i in m_area_list]
    if not area:
        area = '跨一'

    line_data = {}
    date_range = {}
    for area in area_name_list:
        line_data[area] = [
            {"name":"时段一", "data":[]},
            {"name":"时段二", "data":[]},
            {"name":"时段三", "data":[]},
            {"name":"时段四", "data":[]},
        ]
        date_range[area] = []
        sp_list = salePrice_list(area)
        value = sp_list.values()

        for item in value:
            date_range[area].append(item['source_data'][5:])
            for i in range(4):
                line_data[area][i]["data"].append(item['rst'][i])
    return render_template(
        "/DNF/index.html",
        user=current_user,
        line_data=line_data,
        date_range=date_range,
        area_list=area_name_list,
        area=area
    )

@app.route('/buyer_index')
def buyer_index():
    return render_template("/DNF/index.html")

@app.route('/goods_list')
def list_goods():
    return render_template("goods_list.html")

@app.route('/set_config')
def setConfig():
    tkn = request.args.get("jwt", "")
    phone, pwd, msg = _verify_token(tkn)
    if msg:
        return msg
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
