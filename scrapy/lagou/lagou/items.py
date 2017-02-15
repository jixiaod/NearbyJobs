# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class CommpanyItem(scrapy.Item):
    # define the fields for your item here like:

    lagou_url = scrapy.Field()
    name = scrapy.Field()
    short_name = scrapy.Field()
    company_word = scrapy.Field()
    href = scrapy.Field()
    identification = scrapy.Field()
    address = scrapy.Field()
    #pass

