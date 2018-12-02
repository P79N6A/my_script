# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DuowanGifItem(scrapy.Item):
    """
    多玩gif图片item
    """
    page_no = scrapy.Field()
    gif_url = scrapy.Field()
    text = scrapy.Field()
    file_name = scrapy.Field()
    gif_dir = scrapy.Field()

class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
