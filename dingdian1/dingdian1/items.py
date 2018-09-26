# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Dingdian1Item(scrapy.Item):
    # define the fields for your item here like:
    novel_name = scrapy.Field() #定义小说名字
    author = scrapy.Field() #定义小说作者
    name_id = scrapy.Field()#定义小说编号
    chapterurl = scrapy.Field()#定义小说章节地址
    chaptername = scrapy.Field()#定义小说章节名字
    content = scrapy.Field()#定义小说章节内容

