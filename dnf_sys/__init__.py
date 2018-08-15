# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template, redirect, request
from dnf_sys import cfg
import jwt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = cfg.DB_SERVER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

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

@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        phone = request.form.get('phone')
        pwd = request.form.get('pwd')
        jwt_data = {'phone': phone, 'pwd': pwd}
        mc_jwt = cfg.mc_jwt
        jwt_encode_data = jwt.encode(jwt_data, mc_jwt)
        redir_url = '/set_config?jwt=%s' % jwt_encode_data
        return redirect(redir_url)
    return render_template("sign.html")


@app.route('/set_config')
def setConfig():
    tkn = request.args.get("jwt", "")
    phone, pwd, msg = _verify_token(tkn)
    if msg:
        return msg
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
