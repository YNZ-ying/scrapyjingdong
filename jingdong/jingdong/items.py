# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongItem(scrapy.Item):
    # define the fields for your item here like:)
    bookname = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    commentcount = scrapy.Field()
    putlish = scrapy.Field()
    bookurl = scrapy.Field()
    comment = scrapy.Field()
