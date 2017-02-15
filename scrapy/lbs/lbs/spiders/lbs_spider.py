# -*- coding: UTF-8 -*-   

import scrapy
import json
import urlparse
from pprint import pprint
from pymongo import MongoClient
from scrapy.selector import Selector
from scrapy.http import Request
from lbs.items import LbsItem


class LbsSpider(scrapy.Spider):

    name = "lbs"
    allowed_domains = ["http://restapi.amap.com/"]

    def start_requests(self):
        requests = []

        mongo = MongoClient('127.0.0.1', 27017)
        db = mongo.lg

        cursor = db.company.find()

        for company in cursor:
            cid = company['_id'] 

            if not company['address'] and len(company['address'][0]) <= 4:
                continue
            address = company['address'][0]

            url = "http://restapi.amap.com/v3/place/text?key=8325164e247e15eea68b59e89200988b&city=110000&language=zh_cn&platform=JS&logversion=2.0&sdkversion=1.3&keywords=" + address + "&cid=" + str(cid)   
            request = Request(url, 
                headers={
                         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                         'Accept-Encoding':'gzip, deflate, sdch, br',
                         'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
                         'Cache-Control':'no-cache',
                         'Connection':'keep-alive',
                         'Cookie':'guid=8d54-d9ad-f0a5-0444; key=8325164e247e15eea68b59e89200988b',
                         'Host':'restapi.amap.com',
                         'Pragma':'no-cache',
                         'Upgrade-Insecure-Requests':1,
                         'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
                         }, 
                     callback=self.parse_model)
            requests.append(request)
        return requests


    def parse_model(self, response):
        companys = []
        company =  LbsItem()

        jsonBody = json.loads(response.body.decode('utf-8'))
        location = jsonBody['pois'][0]['location']
        tmp = location.split(",");
        lat = float(tmp[0])
        lon = float(tmp[1])

        url=urlparse.urlparse(response._url)
        params=urlparse.parse_qs(url.query,True) 

        company['cid'] = params['cid'][0]
        company['loc'] = [lat,lon]
        companys.append(company)

        #pprint(company)
        return companys 



