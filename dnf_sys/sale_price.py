# -*- coding: utf-8 -*-
import datetime
from flask import request, render_template
from flask_login import login_required, current_user
from dnf_sys import db, app
from dnf_sys.model.sysModel import SalePriceModel


@login_required
@app.route('/saleprice/new', methods=['GET', 'POST'])
def salePrice_new():
    tkn = request.args.get('jwt', '')
    if request.method == 'POST':
        valid_time = request.form.get("valid_time", "")
        price = request.form.get("sale_price", "")
        print('*' * 20)
        print(current_user.username)
        print(valid_time)
        try:
            valid_time = datetime.datetime.strptime(valid_time, '%Y/%m/%d %H:%M')
            price = int(price)
        except Exception as e:
            return render_template('error.html', error=e)
        new_sale_price = SalePriceModel(sale_price=price, valid_time=valid_time)
        db.session.add(new_sale_price)
        db.session.commit()
        return render_template('index.html')
    return render_template('sale_price.html', tkn=tkn)
