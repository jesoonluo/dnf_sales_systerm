#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from flask import Flask, render_template

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
