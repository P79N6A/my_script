#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2018/8/17 下午9:54
@Author  : lizhiran
@Email   : 794339312@qq.com
"""
import requests
import json
from requests.cookies import RequestsCookieJar
import os
import random
import time
import re

class M_Weibo(object):
    login_code = ""
    password = ""
    uid = ""
    homeUrl = ""
    st = ""
    config_time = 0
    can_do_like = True
    can_do_follow = True
    can_do_cmt = True
    face = list()

    def __init__(self, login_code, password):
        self.login_code = login_code
        self.password = password
        self.session = requests.session()
        self.login_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Accept': 'text/html;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Connection': 'keep-alive',
            'Referer': 'https://passport.weibo.cn/signin/login',
            'Host': 'passport.weibo.cn'
        }
        self.__login()
        weibo, follow, fans = self.user_info()
        print("微博:%s,关注：%s,粉丝:%s" % (weibo, follow, fans))

    def __login(self):
        url = r'https://passport.weibo.cn/sso/login'
        # 构造参数字典
        data = {'username': self.login_code,
                'password': self.password,
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
        need_login = True
        # self.__set_cookies()
        # self.__request_config()
        # if self.uid:
        #     need_login = False
        if need_login:
            try:
                # 模拟登录
                login_ret = self.session.post(url=url, data=data, headers=self.login_headers).text
                json.loads(login_ret)['data']['crossdomainlist'].values()
                self.__request_config()
                print("%s 登录成功" % self.login_code)
            except Exception as e:
                print("%s 登录失败"%self.login_code)
                raise e
        else:
            print("%s 已经登录" % self.login_code)

    def __make_headers(self, header=dict()):
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Accept': 'text/html;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Connection': 'keep-alive'
        }
        for k, v in header.items():
            self.session.headers[k] = v

    def __set_cookies(self):
        jar = RequestsCookieJar()
        if os.path.exists('cookies_%s.txt' % self.login_code):
            with open('cookies_%s.txt' % self.login_code, 'r') as f:
                cookies = json.load(f)
                for key in cookies.keys():
                    jar.set(key, cookies[key])
            self.session.cookies = jar

    def __save_cookies(self):
        with open('cookies_%s.txt' % self.login_code, 'w') as f:
            json.dump(self.session.cookies.get_dict(), f)

    def user_info(self):
        return self.__get_user_info(self.uid)

    def __get_user_info(self, uid):
        self.__make_headers({'Referer': 'https://m.weibo.cn/profile/%s' % uid})
        url = 'https://m.weibo.cn/profile/info?uid=%s' % uid
        ret = self.session.get(url).text
        data = json.loads(ret)
        weibo = data['data']['user']['statuses_count']
        follow = data['data']['user']['follow_count']
        fans = data['data']['user']['followers_count']
        return weibo, follow, fans

    def get_follows(self):
        screen_name = ('股票情报员周周',
                       '叶檀',
                       '戴斌',
                       '王思聪',
                       'Mr蒋静',
                       )
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=231093_-_selffollowed'
        user_list = list()
        self.__make_headers({'Referer': 'https://m.weibo.cn/p/index?containerid=231093_-_selffollowed'})
        try:
            ret = self.session.get(url).text
            json_data = json.loads(ret)
            data = json_data['data']['cards']
            for item in data:
                if item.get('title', '') == '全部关注':
                    data = item['card_group']
                    break
            for item in data:
                flag = False
                for button in item['buttons']:
                    if button['relationship'] == 2:
                        flag = True
                        break
                if flag:
                    user = dict()
                    if item['user']['screen_name'] in screen_name:
                        continue
                    user['uid'] = item['user']['id']
                    user['user_screen_name'] = item['user']['screen_name']
                    user_list.append(user)
        except Exception as e:
            print('获取关注列表失败', e)
        return user_list

    def get_friends_mids(self, count):
        url = 'https://m.weibo.cn/feed/friends'
        header = {'Host': 'm.weibo.cn', 'Referer': 'https://m.weibo.cn'}
        self.__make_headers(header)
        friends_mids = dict()
        while len(friends_mids) < count:
            try:
                ret = self.session.get(url).text
                data = json.loads(ret)
                next_cursor = data['data']['next_cursor']
                for item in data['data']['statuses']:
                    mid_data = {
                        'mid': item['mid'],
                        'text': item['text'],
                        'liked': item.get('liked', False),
                        'reposts_count': item['reposts_count'],
                        'comments_count': item['comments_count'],
                        'attitudes_count': item['attitudes_count'],
                        'uid': item['user']['id'],
                        'user_screen_name': item['user']['screen_name'],
                        'user_statuses_count': item['user']['statuses_count'],
                        'user_follow_count': item['user']['follow_count'],
                        'user_followers_count': item['user']['followers_count']
                    }
                    friends_mids[item['mid']] = mid_data
                url = 'https://m.weibo.cn/feed/friends?max_id=%s' % next_cursor
            except Exception as e:
                print('获取关注列表异常', e)
                break
        return friends_mids

    def get_channel_mids(self, channel_code, count):
        base_url = 'https://m.weibo.cn/api/container/getIndex?containerid=%s&openApp=0&since_id=%s'
        header = {'Host': 'm.weibo.cn', 'Referer': 'https://m.weibo.cn'}
        self.__make_headers(header)
        channel_mids = dict()
        url = base_url % (channel_code, '0')
        while len(channel_mids) < count:
            try:
                ret = self.session.get(url).text
                data = json.loads(ret)
                since_id = data['data']['cardlistInfo']['since_id']
                for item in data['data']['cards']:
                    mid_data = {
                        'mid': item['mblog']['mid'],
                        'text': item['mblog']['text'],
                        'liked': item['mblog'].get('liked', False),
                        'reposts_count': item['mblog']['reposts_count'],
                        'comments_count': item['mblog']['comments_count'],
                        'attitudes_count': item['mblog']['attitudes_count'],
                        'uid': item['mblog']['user']['id'],
                        'user_screen_name': item['mblog']['user']['screen_name'],
                        'user_statuses_count': item['mblog']['user']['statuses_count'],
                        'user_follow_count': item['mblog']['user']['follow_count'],
                        'user_followers_count': item['mblog']['user']['followers_count']
                    }
                    channel_mids[item['mblog']['mid']] = mid_data
                url = base_url % (channel_code, since_id)
            except Exception as e:
                print('获取关注列表异常', e)
                break
        return channel_mids

    def get_cmt(self, mid, count=20):
        cmt_url = "https://m.weibo.cn/api/comments/show?id=%s&page=%s"
        cookies = self.session.cookies.get_dict()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
        }
        self.__make_headers()
        cids_list = list()
        cmt_list = list()
        page_no = 1
        while len(cids_list) < count:
            url = cmt_url % (mid, page_no)
            try:
                print(url)
                # ret = requests.get(url, headers = headers, cookies = cookies).text
                ret = self.session.get(url).text
                print(ret)
                ret_json = json.loads(ret)
                if ret_json['ok'] == 0:
                    break
                data = ret_json['data']['data']
                for item in data:
                    page_no += 1
                    if not item['user']['following']:
                        cids = dict()
                        cids['uid'] = item['user']['id']
                        if self.uid == str(cids['uid']):
                            continue
                        weibo, follow, fans = self.__get_user_info(cids['uid'])
                        if follow/fans > 2:
                            continue
                        cids['cid'] = item['id']
                        cids['liked'] = item.get('liked', False)
                        cids['mid'] = mid
                        cids['user_screen_name'] = item['user']['screen_name']
                        if cids['uid'] not in cids_list:
                            cmt_list.append(cids)
                            cids_list.append(cids['uid'])
            except Exception as e:
                print(ret, e)
                break
        return cmt_list

    def __get_face(self):
        url = 'https://h5.sinaimg.cn/m/weibo-lite/js/25.2ea224af.js'
        header = {
            'Host': '',
            'Referer': ''
        }
        self.__make_headers()
        resp = self.session.get(url)
        resp.encoding = 'utf-8'
        ret = resp.text
        s = re.match(r'.*o.exports=({".*others"}).*', ret).group(1)
        s = s.replace('class', '"class"').replace('source', '"source"').replace('group', '"group"')
        s = s.replace('},"', "},").replace('":{', ':{').replace('},', '},"').replace(':{', '":{') + '}'
        data = json.loads(s)
        return list(data.keys())

    def __get_cmt_content_random(self, mid):
        cmt_url = "https://m.weibo.cn/api/comments/show?id=%s&page=%s"
        self.__make_headers()
        url = cmt_url % (mid, 1)
        self.face = self.__get_face() if not self.face else self.face
        face_text = '[' + self.face[random.randint(0, len(self.face)-1)] + ']'
        content = ['消灭0评论', '路过...', '互动一下', '过来看看', 'just评论一下', '赞一个', '你好', '多多关注', '粉一下？', '']
        text = content[random.randint(0, len(content)-1)]
        filter_word = ['回复', 'img', 'http', 'url']
        try:
            ret = self.session.get(url)
            ret_json = json.loads(ret.text)
            data = ret_json['data']['data']
            for item in data:
                is_filter = False
                for word in filter_word:
                    if word in item['text']:
                        is_filter = True
                        break
                if not is_filter and not item.get('pic', ''):
                    text = item['text']
        except Exception as e:
            print(ret.text, e)
        return text + face_text

    def __save_cmt(self, id):
        with open('comment_id_%s.txt' % self.login_code, 'a+') as f:
            f.write('%s\n' % id)

    def __get_cmt(self):
        with open('comment_id_%s.txt' % self.login_code, 'r') as f:
            lines = f.readlines()
        return map(lambda x: x.replace('\n', ''), lines)

    def do_cmt(self, mid):
        if mid in self.__get_cmt() or not self.can_do_cmt:
            return False
        cmt_url = 'https://m.weibo.cn/api/comments/create'
        content = self.__get_cmt_content_random(mid)
        data = {
            'content': content,
            'mid': mid,
            'st': self.st
        }
        try:
            ret = self.session.post(cmt_url, data=data).text
            data = json.loads(ret)
            if data.get('ok', 0) == 1:
                print('评论成功mid:%s, text:%s' % (mid, content))
                self.__save_cmt(mid)
            else:
                print('评论失败, %s' % ret)
                if str(data['errno']) in ('100005', '100006', '20016', '20210'):
                    self.can_do_cmt = False
        except Exception as e:
            print('评论异常', e)

    def do_like(self, mid_data):
        if mid_data['liked'] or not self.can_do_like:
            return False
        like_url = 'https://m.weibo.cn/api/attitudes/create'
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Length': '44',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'm.weibo.cn',
            'MWeibo-Pwa': '1',
            'Origin': 'https://m.weibo.cn',
            'Referer': 'https://m.weibo.cn/',
        }
        self.__make_headers(header)
        data = {
            'attitude': 'heart',
            'id': mid_data['mid'],
            'st': self.st
        }
        try:
            ret = self.session.post(like_url, data=data).text
            data = json.loads(ret)
            if data.get('ok', 0) == 1:
                print('点赞成功mid:%s' % mid_data['mid'])
                return True
            else:
                print('点赞失败, %s' % data['msg'])
                self.can_do_like = False
                return False
        except Exception as e:
            print('点赞异常', e)
            return False

    def do_report(self, mid_data):
        if mid_data['reposts_count'] < 100:
            return
        mid = mid_data['mid']
        text = mid_data['text']
        report_url = 'https://m.weibo.cn/api/statuses/repost'
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Length': '44',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'm.weibo.cn',
            'MWeibo-Pwa': '1',
            'Origin': 'https://m.weibo.cn',
            'Referer': 'https://m.weibo.cn/compose/repost?id=%s' % mid,
        }
        self.__make_headers(header)
        data = {
            'dualPost': '1',
            'id': mid,
            'mid': mid,
            'content': text,
            'st': self.st
        }
        try:
            ret = self.session.post(report_url, data=data).text
            data = json.loads(ret)
            if data.get('ok', 0) == 1:
                print('转发成功mid:%s' % mid)
            else:
                print('转发失败, %s' % data['msg'])
        except Exception as e:
            print('转发异常', e)

    def do_follow(self, user):
        if not self.can_do_follow:
            return False
        url = 'https://m.weibo.cn/api/friendships/create'
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Length': '44',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'm.weibo.cn',
            'MWeibo-Pwa': '1',
            'Origin': 'https://m.weibo.cn',
            'Referer': 'https://m.weibo.cn/',
        }
        self.__make_headers(header)
        data = {
            'uid': user['uid'],
            'st': self.st
        }
        try:
            ret = self.session.post(url, data=data).text
            data = json.loads(ret)
            if data.get('ok', 0) == 1:
                print('加关注成功uid:%s, 昵称:%s' % (user['uid'], user['user_screen_name']))
                return True
            else:
                print('加关注失败, %s' % data['msg'])
                self.can_do_follow = False
                return False
        except Exception as e:
            print('加关注异常', e)
            return False

    def destory_follow(self, user):
        url = 'https://m.weibo.cn/api/friendships/destory'
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Length': '44',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'm.weibo.cn',
            'MWeibo-Pwa': '1',
            'Origin': 'https://m.weibo.cn',
            'Referer': 'https://m.weibo.cn/profile/%s' % user['uid'],
        }
        self.__make_headers(header)
        data = {
            'uid': user['uid'],
            'st': self.st
        }
        try:
            ret = self.session.post(url, data=data).text
            data = json.loads(ret)
            if data.get('ok', 0) == 1:
                print('取消关注成功uid:%s, 昵称:%s' % (user['uid'], user['user_screen_name']))
            else:
                print('取消关注失败%s, %s' % (user['uid'], data['msg']))
        except Exception as e:
            print('取消关注异常', e)

    def do_cmt_like(self, cid_data):
        if cid_data['liked'] or not self.can_do_like:
            return False
        like_url = 'https://m.weibo.cn/api/likes/update'
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Length': '44',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'm.weibo.cn',
            'MWeibo-Pwa': '1',
            'Origin': 'https://m.weibo.cn',
            'Referer': 'https://m.weibo.cn/detail/%s' % cid_data['mid'],
        }
        self.__make_headers(header)
        data = {
            'type': 'comment',
            'id': cid_data['cid'],
            'st': self.st
        }
        try:
            ret = self.session.post(like_url, data=data).text
            data = json.loads(ret)
            if data.get('ok', 0) == 1:
                print('点赞成功cid:%s' % cid_data['cid'])
                return True
            else:
                print('点赞失败, %s' % data['msg'])
                self.can_do_like = False
                return False
        except Exception as e:
            print('点赞异常', e)
            return False

    def __request_config(self):
        url = 'https://m.weibo.cn/api/config'
        header = {
            'Host': 'm.weibo.cn',
            'Referer': 'https://m.weibo.cn'
        }
        self.__make_headers(header)
        try:
            ret = self.session.get(url).text
            data = json.loads(ret)
            self.st = data['data']['st']
            self.uid = data['data']['uid']
            self.__save_cookies()
        except Exception as e:
            print('request config', e)

    def __request_unread(self):
        url = 'https://m.weibo.cn/api/remind/unread?t=%s' % str(int(time.time() * 1000))
        header  = {
            'Host': 'm.weibo.cn',
            'Referer': 'https://m.weibo.cn/sw.js'
        }
        self.__make_headers(header)
        self.session.get(url)

    def sleep(self, l, r):
        if self.config_time > 6 * 60:
            self.__request_config()
            self.can_do_like = True
        self.__request_unread()
        d = random.randint(l, r)
        print('sleep %s seconds...' % d)
        time.sleep(d)

def main():
    m = M_Weibo('16601169526', 'yy12y090812y')
    # friends_mids = m.get_friends_mids(10)
    # for mid, data in friends_mids.items():
    #     m.do_cmt(mid)
    #     if m.do_like(data):
    #         m.sleep(5, 20)
    channel_mids = m.get_channel_mids('102803_ctg1_4388_-_ctg1_4388', 10)
    for mid, data in channel_mids.items():
        m.do_cmt(mid)
        m.do_like(data)
        m.do_report(data)
        cmt_list = m.get_cmt(mid, 10)
        for cmt_data in cmt_list:
            if m.do_cmt_like(cmt_data):
    #         m.do_follow(user)
                m.sleep(5, 30)

if __name__ == '__main__':
    main()
    # m = M_Weibo('16601169526', 'yy12y090812y')
    # m = M_Weibo('yuyan235813', 'yy12y090812y')
    # mids = m.get_friends_mids(10)
    # for mid, data in mids.items():
    #     m.do_cmt(mid)
    #     # m.do_like(mid)
    #     m.do_report(data)
    #     time.sleep(random.randint(1, 3))
    #     print(mid)
    # mids = m.get_channel_mids('102803_ctg1_4388_-_ctg1_4388', 10)
    # print(mids.keys())
    # tt = m.session.get('https://m.weibo.cn/api/comments/show?id=4312847473129020&page=1').text
    # print(tt)
    # m.do_follow({'uid': '1935856651', 'user_screen_name': '搞笑视频大推荐'})
    # m.destory_follow({'uid': '1935856651', 'user_screen_name': '搞笑视频大推荐'})
    # print(m.get_follows())
