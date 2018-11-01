#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2018/10/30 下午3:37
@Author  : lizhiran
@Email   : 794339312@qq.com
"""
import requests
# header = {'Authorization':'TAuth2 token="OXQNVTONRSTTXNXONYNZPSSXOSRNWUVSWPXNXNX7GkaH%40EblV",param="uid%3D1642909335",sign="t8wSYgPNtSbKwhVn9ZV9K3Z4vDg%3D"'}
# url = 'http://i2.api.weibo.com/2/statuses/is_read_batch.json?platform_type=1&source=3086104566&uid=1595553794&ids=4299099848857794,4298727437390957,4297643515241558'
# ret = requests.get(url=url, headers=header)
# print(ret.text)


url='http://controlcenter.ds.sina.com.cn/waic/hbase/case/insert?'
# param={'keyId': 'mainpagerecom|1540828800|hot_uv', 'value': '23031385', 'business': 'main_page_statistic'}
param={'keyId': 'iarate|1540828800|default', 'value': '8.925804660529082', 'business': 'expand_reading_ABtest'}
ret=requests.post(url, data=param)
print(ret.text)

# param='keyId=iarate%7c1541053192%7cdefault&value=8.925804660529082&business=expand_reading_ABtest'
# ret=requests.get(url+param)
# print(ret.text)