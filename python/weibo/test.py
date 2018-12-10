#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2018/8/17 下午9:54
@Author  : lizhiran
@Email   : 794339312@qq.com
"""

# -*- coding: utf-8 -*-
import requests


base_url = 'https://m.weibo.cn/api/comments/show?id=4315258593849328&page={page}'
cookies = {'Cookie':'_T_WM=fc4eb4303824895324ba8458ea2c6288; WEIBOCN_FROM=1110006030; SUB=_2A25xD6hlDeRhGeBG7VoV9yvPyziIHXVS88gtrDV6PUJbkdAKLUn1kW1NQevcmZ53K5mAIcgQaJxsatd55Hif6xp-; SUHB=0C1CxtR24lQbrC; SCF=AuEqpYFNUv5xm3XWz3CBY1b1sr4KodwmFRGI4OsfD7JwOK4r-ZAzQmssA4O0GPji5fHNF5D3K9e0t1tKUfxjL_o.; SSOLoginState=1544280117; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4315277699167312%26luicode%3D20000061%26lfid%3D4315277699167312'}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}

for i in range(0,1):
    try:
        url = base_url.format(page=i)
        resp = requests.get(url, headers=headers, cookies=cookies)
        print(resp.text)
        jsondata = resp.json()

        data = jsondata.get('data')
        for d in data:
            created_at = d.get("created_at")
            source = d.get("source")
            username = d.get("user").get("screen_name")
            comment = d.get("text")
            print((username,source,comment))
    except:
        print('*'*1000)
        pass