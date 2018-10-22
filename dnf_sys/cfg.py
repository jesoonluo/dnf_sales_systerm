# -*- coding: utf-8 -*-
APP_NAME = 'DnfSalesSys'
DB_SERVER = 'mysql+pymysql://dnf:dddd@localhost/dnf_sys?charset=utf8mb4'
mc_jwt = 'jwmy2ol8'
secret_key = 'liqi secret'

order_status = {
    'wait_pay': '待支付',
    'have_pay': '已支付',
    'have_pic': '已拍照',
    'have_pro': '已拍货',
    'success': '已完成'
}
