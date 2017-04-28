# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Test2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 姓名
    name = scrapy.Field()
    # 出生日期
    birthday = scrapy.Field()
    # 国籍
    nation = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 职业
    job = scrapy.Field()
