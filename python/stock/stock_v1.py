#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2018/8/17 下午9:54
@Author  : lizhiran
@Email   : 794339312@qq.com
"""
import tushare as ts

ts.set_token('da8eca9478ef3672be8bbc4b81dad1d356f7e2ce9a43749568cb6da7')

pro = ts.pro_api()

# df = pro.fund_basic(market='E')

df = pro.fund_portfolio(ts_code='001753.OF')

print(df)