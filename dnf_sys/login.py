# -*- coding: utf-8 -*-

import json
from flask import request, render_template, Response, redirect
from dnf_sys import app
from dnf_sys.model.userModel import UserModel
from flask_login import login_user


"""
@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        phone = request.form.get('phone')
        pwd = request.form.get('pwd')
        jwt_data = {'phone': phone, 'pwd': pwd}
        mc_jwt = cfg.mc_jwt
        jwt_encode_data = jwt.encode(jwt_data, mc_jwt)
        redir_url = '/index?jwt=%s' % jwt_encode_data
        return redirect(redir_url)
    return render_template("sign.html")
"""

@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        phone = request.form.get('phone')
        pwd = request.form.get('pwd')
        params = {
            'username': phone,
            'password': pwd,
        }
        ret = UserModel.login(**params)
        if ret['errcode'] == 0:
            user = ret.pop('data')
            if user.is_active() is False:
                return render_template('error.html', error='用户已被封,请联系管理员解锁')
            login_user(user)
            # set cookie
            ret = json.dumps(ret)
            resp = Response(ret)
            resp.set_cookie(key='jwmy-islogin',value='true')
            return redirect('/index')
        else:
            return render_template('error.html', error=ret['errmsg'])
    return render_template("sign.html")


