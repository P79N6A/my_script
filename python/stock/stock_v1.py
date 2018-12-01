#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2018/8/17 下午9:54
@Author  : lizhiran
@Email   : 794339312@qq.com
"""
import tushare as ts

ts.set_token('da8eca9478ef3672be8bbc4b81dad1d356f7e2ce9a43749568cb6da7')

api = ts.pro_api()

# df = pro.fund_basic(market='E')

# df = ts.pro_bar(pro_api=api, ts_code='603986.SH', adj='qfq', freq='60', start_date='20181015', end_date='20181016')
#
# print(df)

# df = ts.get_hist_data('881154', ktype='60', start='2018-11-15', end='2018-11-16')
# print(df.ix[:,4:8])
#
df = ts.pro_bar(pro_api=api, ts_code='801024.SI', adj='qfq', start_date='20180101', end_date='20181011')
df = api.index_basic(market='CSI')
print(df)