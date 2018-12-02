#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2018/8/17 下午9:54
@Author  : lizhiran
@Email   : 794339312@qq.com
"""
from SinaWeibo import Weibo
import json
import time
import re
import requests


def get_weibo_session():
    url = r'https://passport.weibo.cn/sso/login'
    # 构造参数字典
    data = {'username': '16601169526',
            'password': 'yy12y090812y',
            'savestate': '1',
            'r': r'',
            'ec': '0',
            'pagerefer': '',
            'entry': 'mweibo',
            'wentry': '',
            'loginfrom': '',
            'client_id': '',
            'code': '',
            'qq': '',
            'mainpageflag': '1',
            'hff': '',
            'hfp': ''}
    # headers，防屏
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Accept': 'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Connection': 'close',
        'Referer': 'https://passport.weibo.cn/signin/login',
        'Host': 'passport.weibo.cn'
        }
    # 模拟登录
    session = requests.session()
    session.post(url=url, data=data, headers=headers)
    return session


def following(wb, uid):
    data={
        "uid": uid,
        "objectid": "",
        "f": "1",
        "extra": "",
        "refer_sort": "",
        "refer_flag": "1005050001_",
        "location": "page_100505_home",
        "oid": "1871110130",
        "wforce": "1",
        "nogroup": "1",
        "fnick": "",
        "refer_lflag": "",
        "refer_from": "profile_headerv6",
        "template": "7",
        "special_focus": "1",
        "isrecommend": "1",
        "is_special": "0",
        "redirect_url": "%252Fp%252F1005056868475304%252Fmyfollow%253Fgid%253D4312028581482291%2523place",
        "_t": "0"
    }
    now_time = int(time.time() * 1000)
    url = "https://weibo.com/aj/f/followed?ajwvr=6&__rnd=%s" % now_time
    wb.session.headers["Host"] = "weibo.com"
    wb.session.headers["Origin"] = "https://weibo.com"
    wb.session.headers['Referer'] = "https://weibo.com/gifmonster?is_hot=1&noscale_head=1"
    ret = wb.session.post(url, data=data).text
    ret_dict = json.loads(ret)
    if ret_dict['code'] == '100000':
        print("uid=%s, 加关注成功" % uid)
    else:
        print("uid=%s, 加关注失败" % uid)


def get_cmt_user_id(session, mid):
    cmt_url = "https://m.weibo.cn/api/comments/show?id=%s&page=%s"
    user_list = []
    for i in range(1, 3):
        url = cmt_url % (mid, i)
        ret = session.get(url)
        print(url)
        if not ret.text or ret.status_code != 200:
            print('request error')
            continue
        try:
            ret_json = json.loads(ret.text)
        except Exception:
            print(url)
            print(ret.text)

        data = ret_json['data']['data']
        for item in data:
            if not item['user']['following']:
                user_list.append(item['user']['id'])
    user_list = list(set(user_list))
    print(user_list)
    return user_list


def postImage(wb):
    base_dir = "H:\\gif\\duowan\\100003"
    import os
    with open(os.path.join(base_dir, "test.txt"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            line_arr = line.split("\t")
            wb.postImage(line_arr[0], os.path.join(base_dir, line_arr[1]))
            time.sleep(150)


if __name__ == '__main__':
    # mid="4312847473129020"
    # session = get_weibo_session()
    wb = Weibo("16601169526", "yy12y090812y")
    # uid_list = get_cmt_user_id(session, mid)
    # for uid in uid_list:
    #     time.sleep(1)
    #     following(wb, uid)

    postImage(wb)


    # get_cmt_user_id('4304528373262567')
    # wb= Weibo("16601169526", "yy12y090812y")
    # wb.postMessage("0.2测试1:文本")
    # time.sleep(1)
    # wb.postImage("狗狗真好！", "H:\\gif\\duowan\\100003\\27eedc67ab7ecc6529a5f7ec2cc4b963.gif")
    # time.sleep(1)
    # wb.postImage("0.2测试3:多张图片","/Downloads/4.png","/Downloads/5.jpg")
    #
    # # 我的关注
    # pageNum = 1
    # followList, hasNext = wb.getFollowList(pageNum)
    # print(followList)
    # while hasNext == True:
    #     pageNum = pageNum + 1
    #     followList, hasNext = wb.getFollowList(pageNum)
    #     print(followList)
    #
    # # 我的粉丝
    # pageNum = 1
    # fansList , hasNext = wb.getFansList(pageNum)
    # print(fansList)
    # while hasNext == True:
    #     pageNum = pageNum + 1
    #     fansList, hasNext = wb.getFansList(pageNum)
    #     print(fansList)
    #
    # # 我的微博
    # blogList = wb.getMyBlogList(1)
    # for blog in blogList:
    #     print(blog)


