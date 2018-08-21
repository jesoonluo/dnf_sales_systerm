# -*- coding: utf-8 -*-
from flask import request, render_template
from dnf_sys import db, app
from dnf_sys.model.userModel import SalePriceModel

@app.route('/saleprice/new')
def salePrice_new():
    price = request.args.get("price", "")
    if not price:
        return '请输入利率值'
    new_sale_price = SalePriceModel(sale_price=price)
    db.session.add(new_sale_price)
    db.session.commit()
    return render_template('index.html')
