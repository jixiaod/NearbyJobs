# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from pprint import pprint
from bson.objectid import ObjectId

class SpiderPipeline(object):
    def process_item(self, item, spider):
        mongo = MongoClient('127.0.0.1', 27017)
        db = mongo.jobs
        db.company.insert({
                    "lagou_url": item['lagou_url'], 
                    "name": item['name'],
                    "short_name": item['short_name'],
                    "company_word": item['company_word'],
                    "href": item['href'],
                    "identification": item['identification'],
                    "address": item['address']})
        return item
