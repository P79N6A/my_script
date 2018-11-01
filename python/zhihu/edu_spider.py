#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2018/10/30 下午3:01
@Author  : lizhiran
@Email   : 794339312@qq.com
"""
import os

from zhihu_oauth import ZhihuClient


TOKEN_FILE = 'token.pkl'


def login_zhihu():
    """
    登录知乎
    :return:
    """
    client = ZhihuClient()
    if os.path.isfile(TOKEN_FILE):
        client.load_token(TOKEN_FILE)
    else:
        client.login_in_terminal()
        client.save_token(TOKEN_FILE)
    return client


if __name__ == '__main__':
    client = login_zhihu()
    topic = client.topic(19564381)
    print(topic.name)
    # questions = topic.unanswered_questions
