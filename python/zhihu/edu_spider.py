#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2018/10/30 下午3:01
@Author  : lizhiran
@Email   : 794339312@qq.com
"""
import os

from zhihu_oauth import ZhihuClient
from sqllite_util import EasySqlite


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
    topic_id = 19564381
    topic = client.topic(topic_id)
    print(topic)
    questions = topic.unanswered_questions
    db = EasySqlite('zhihu.db')
    sql_tmp = 'replace into questions values(?,?,?,?,?,?)'
    for question in questions:
        if question.answer_count < 10:
            continue
        row = [question.id, question.title, question.follower_count, question.answer_count, question.comment_count,
               topic_id]
        print(row)
        ret = db.update(sql_tmp, args=row)
        if not ret:
            print('insert error!')
        else:
            print('insert success!')
