#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2018/8/17 下午9:54
@Author  : lizhiran
@Email   : 794339312@qq.com
"""
import scrapy
import time
import json
from spider.items import DuowanGifItem
import os
import urllib.parse as urlparse


class GifSpider(scrapy.Spider):
    name = "duowan_gif"
    allowed_domains = ["tu.duowan.com"]
    page_no = 137925
    now_time = int(time.time()*1000)
    gif_dir = "G:\\gif\\duowan\\%s"
    url_tmp = "http://tu.duowan.com/index.php?r=show/getByGallery/&gid=%s&_=%s"
    start_urls = [
        "http://tu.duowan.com/index.php?r=show/getByGallery/&gid=137925&_=%s" % now_time,
        ]

    def parse(self, response):
        self.now_time = int(time.time() * 1000)
        url = self.url_tmp % (self.page_no, self.now_time)
        self.page_no -= 1
        yield scrapy.Request(url, callback=self.parse_dir_content)

    def parse_dir_content(self, response):
        ret = json.loads(response.body)
        if 'GIF' in ret['gallery_title']:
            print(response.url)
            dic = urlparse.parse_qs(response.url)
            page_no = dic['gid'][0]
            print(page_no)
            for item in ret['picInfo']:
                gif_item = DuowanGifItem()
                gif_item['page_no'] = page_no
                gif_item['gif_url'] = item['url']
                gif_item['text'] = item['add_intro']
                gif_item['gif_dir'] = self.gif_dir % page_no
                gif_item['file_name'] = os.path.basename(item['url'])
                os.makedirs(gif_item['gif_dir'], exist_ok=True)
                yield gif_item
        while self.page_no >= 118428:
            self.now_time = int(time.time() * 1000)
            url = self.url_tmp % (self.page_no, self.now_time)
            self.page_no -= 1
            yield scrapy.Request(url, callback=self.parse_dir_content)
