# -*- coding: utf-8 -*-
import jwt
import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template, redirect, request
from flask_login import LoginManager, login_required
from dnf_sys import cfg


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = cfg.DB_SERVER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_NAME'] = 'Ssession'
app.config['REMEMBER_COOKIE_DURATION'] = datetime.timedelta(hours=2)
app.secret_key = cfg.secret_key
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

import dnf_sys.sale_price
import dnf_sys.login
from dnf_sys.model.userModel import UserModel

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(user_id)

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
def index():
    return render_template("index.html")

@app.route('/seller_index')
def seller_index():
    return render_template("seller_index.html")

@app.route('/buyer_index')
def buyer_index():
    return render_template("index.html")

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
