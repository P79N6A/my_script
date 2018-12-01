#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2018/8/17 下午9:54
@Author  : lizhiran
@Email   : 794339312@qq.com
"""
from selenium import webdriver

browser = webdriver.Chrome(executable_path='H:\program\chromedriver\chromedriver.exe')
browser.get('http://www.baidu.com/')