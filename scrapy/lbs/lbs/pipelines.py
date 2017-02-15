# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from pprint import pprint
from bson.objectid import ObjectId

class LbsPipeline(object):
    def process_item(self, item, spider):

        mongo = MongoClient('127.0.0.1', 27017)
        db = mongo.jobs
        db.company.update({"_id":ObjectId(str(item['cid']))}, {"$set":{"loc":item['loc']}})

        return item
