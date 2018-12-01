#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2018/10/30 下午3:01
@Author  : lizhiran
@Email   : 794339312@qq.com
"""
import os

from zhihu_oauth import ZhihuClient, Answer
from sqllite_util import EasySqlite


class ZhiHu(object):
    TOKEN_FILE = 'token.pkl'

    def __init__(self):
        """
        初始化
        """
        self.login_zhihu()
        self.db = EasySqlite('zhihu.db')

    def login_zhihu(self):
        """
        登录知乎
        :return:
        """
        self.client = ZhihuClient()
        if os.path.isfile(self.TOKEN_FILE):
            self.client.load_token(self.TOKEN_FILE)
        else:
            self.client.login_in_terminal()
            self.client.save_token(self.TOKEN_FILE)

    def save_quesions(self, topic_id):
        """
        保存话题下的问题
        :param topic_id:
        :return:
        """
        topic = self.client.topic(topic_id)
        print(topic)
        questions = topic.unanswered_questions
        sql_tmp = 'replace into questions values(?,?,?,?,?,?)'
        for question in questions:
            if question.answer_count < 10:
                continue
            row = [question.id, question.title, question.follower_count, question.answer_count, question.comment_count,
                   topic_id]
            print(row)
            ret = self.db.update(sql_tmp, args=row)
            if not ret:
                print('insert error!')
            else:
                print('insert success!')

    def save_answer_info(self, question_id):
        """
        保存指定问题的答案概况
        :param question_id:
        :return:
        """
        question = self.client.question(question_id)
        print(question.title)
        answers = question.answers
        for answer in answers:
            print(answer.comment_count, answer.excerpt, answer.question, answer.thanks_count,
                  answer.voteup_count)
            answer.save()
            break
        # sql_tmp = 'replace into questions values(?,?,?,?,?,?)'
        # for question in questions:
        #     if question.answer_count < 10:
        #         continue
        #     row = [question.id, question.title, question.follower_count, question.answer_count, question.comment_count,
        #            topic_id]
        #     print(row)
        #     ret = self.db.update(sql_tmp, args=row)
        #     if not ret:
        #         print('insert error!')
        #     else:
        #         print('insert success!')

    def to_md(self, topic, file_name):
        sql = "select * from questions where topic_id = '%s' order by follower_count desc limit 1000" % topic
        ret = self.db.query(sql)
        line_tmp = "%s. [%s](https://www.zhihu.com/question/%s) 关注数：%s 回答数：%s 评论数：%s<br>\n"
        i = 1
        with open(file_name, 'w', encoding='utf8') as f:
            for item in ret:
                line = line_tmp % (i, item['title'], item['id'], item['follower_count'], item['answer_count'], item['comment_count'])
                f.write(line)
                i += 1



if __name__ == '__main__':
    client = ZhiHu()
    # 家庭教育
    # client.save_answer_info(20018541)
    # 儿童教育
    # client.save_quesions(19556671)
    client.to_md(19556671, 'children_questions.md')
