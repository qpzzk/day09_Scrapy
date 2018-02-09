# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QianmuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

#设置好返回的字段，设置了才能抓取得到
class UniversityItem(scrapy.Item):
    name=scrapy.Field()
    rank=scrapy.Field(serializer=int)
    country=scrapy.Field()
    state=scrapy.Field()
    city=scrapy.Field()
    undergraduate_num=scrapy.Field()
    postgraduate_num=scrapy.Field()
    website=scrapy.Field()
