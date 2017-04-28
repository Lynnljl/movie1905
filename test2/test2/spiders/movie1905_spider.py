#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/26 下午19:21
# @Author  : Lynn
# @File    : movie1905_spider.py
# @Desc    :
import scrapy
from urlparse import urljoin
from scrapy.selector import Selector

from scrapy.spiders import Spider
from test2.items import Test2Item

class Movie1905Spider(scrapy.Spider):

    name = 'movie1905'
    allowed_domais = ["1905.com"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    #一级url
    SITE_URL = "http://www.1905.com"
    #入口
    start_urls = {
        "http://www.1905.com/mdb/film/stars/enindex-A?p=1"
    }

    #目录页面分析器
    def parse(self, response):
        selector = Selector(response)
        SITE_URL = "http://www.1905.com"
        '''拿到页面上的演员详情页面链接，给内容解析页面使用，如果有下一页，则调用本身parse（）'''
        self.log("=========目===录====页===面===url===========| %s |" %response.url)
        star_urls = response.xpath("//div[@class='starsName']/a")
        for url in star_urls:
            #print star_urls
            url = urljoin(SITE_URL, url.xpath("@href").extract()[0])
            # 将得到的url传给单页面分析器处理---->parse_star()
            yield scrapy.Request(url, callback=self.parse_star, headers=self.headers)

        # 判断下一页是否存在，如果存在，则继续

        next_pages_url = selector.xpath("//div[@id='new_page']/a/@href").extract()
        if next_pages_url:
            next_pages_url = next_pages_url[0]
            next_page = urljoin(SITE_URL, next_pages_url)
            self.log('==============next_page: %s====================' % next_page)
            # 将 「下一页」的链接传递给自身，并重新分析
            yield scrapy.Request(url=next_page, callback=self.parse, headers=self.headers)


    #单页面分析器

    def parse_star(self, response):
        '''将得到的演员单页面URL进行取值处理'''
        #self.log('star_detail_url: %s' % response.url)
        item = Test2Item()

        name = response.xpath("//div[@class='sbg01']/h1/a/text()").extract()[0]
        birthday = response.xpath("//div[@class='mt08']/p[1]/span/text()").extract()[0]
        nation = response.xpath("//div[@class='mt08']/p[2]/span[@class='g1color']/text()").extract()
        # nation 可能为空，需进行判断
        if nation:
            nation = nation[0]
        else:
            nation = '未知'


        job = response.xpath("//div[@class='mt08']/p[3]/span/text()").extract()
        if job:
            job = job[0]
        else:
            job = 'None'
        score = response.xpath("//div[@class='st_score_r']/div[@id='z0']/div[@class='starMINI fl']/dt[@id='studyplay_extend1_0']/b[@id='studyplay_extend1_0']/text()").extract() + response.xpath("//div[@calss='st_score_r']/div[@id='z0']/div[@class='starMINI fl']/dt[@id='studyplay_extend1_0']/small[@id='score_S']/text()").extract()
        # score 可能为空，需判断
        if score:
            score = score[0]
        else:
            score = 'None'

        # 赋值
        item['name'] = name
        item['birthday'] = birthday
        item['nation'] = nation
        item['job'] = job
        item['score'] = score


        yield item


