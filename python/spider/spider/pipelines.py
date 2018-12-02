# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spider.items import DuowanGifItem
from urllib import request
import os

class SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class DouwanPipeline(object):
    def process_item(self, item, spider):
        if item['gif_url']:
            gif_name = os.path.join(item['gif_dir'], item['file_name'])
            request.urlretrieve(item['gif_url'], gif_name)
            with open(os.path.join(item['gif_dir'], 'readme.txt'), 'a') as f:
                f.write('%s\t%s\t%s\n' % (item['text'], item['file_name'], item['gif_url']))
        else:
            raise DuowanGifItem(item)
        return item
    def close_spider(self, spider):
        print("！！！！！！！已爬取完毕，nice work！！！！！！！！")