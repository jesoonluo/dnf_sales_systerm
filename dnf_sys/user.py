# -*- coding: utf-8 -*-

import json
from flask import request, render_template, Response, redirect, jsonify
from dnf_sys import app, db
from dnf_sys.model.userModel import UserModel, UserDetailModel
from flask_login import login_user, current_user, login_required, logout_user
from dnf_sys.helper import is_manager, get_area_list


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
                return u'用户已被封,请联系管理员解锁'
            login_user(user)
            # set cookie
            ret = json.dumps(ret)
            resp = Response(ret)
            resp.set_cookie(key='jwmy-islogin',value='true')
            return redirect('index')
        else:
            return jsonify(ret)
    return render_template("sign.html")


@app.route('/user_list', methods=['GET'])
@login_required
def user_list():
    user_list = UserModel.query.all()
    rst = []
    for user in user_list:
        user = user.to_dict()
        user_detail = UserDetailModel.query.filter_by(user_id=user['id']).first()
        if user_detail:
            user['lvl'] = user_detail.lvl
        else:
            user['lvl'] = 0
        if user['id'] != current_user.id and not is_manager(user['id']):
            rst.append(user)
    return render_template('user_list.html', user_list=rst, user=current_user, area_list=get_area_list())


@app.route('/user/Op_user', methods=['GET', 'POST'])
@login_required
def opUser():
    user_id = request.args.get('id','')
    op = request.args.get('op', '')
    valid_op = ['lock', 'unlock']
    if op not in valid_op or not op:
        ret = {
            'errcode': '4',
            'emsg': 'operate forbidden!'
        }
        return jsonify(ret)
    if user_id:
        m_user = UserModel.query.get(int(user_id))
        if op == 'lock':
            m_user.active = False
        elif op == 'unlock':
            m_user.active = True
        db.session.commit()
    return redirect('/user_list')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/sign')

