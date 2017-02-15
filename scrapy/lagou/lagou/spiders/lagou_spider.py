# -*- coding: UTF-8 -*-   

import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from lagou.items import CommpanyItem


class LagouSpider(scrapy.Spider):

    name = "lagou"
    allowed_domains = ["www.lagou.com"]
    website_possible_httpstatus_list = [404]
    handle_httpstatus_list = [404]

    def start_requests(self):
        requests = []
        for i in range(7, 18000):

            url = 'https://www.lagou.com/gongsi/'+ str(i) +'.html'

            request = Request(url, 
                    headers={
                         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                         'Accept-Encoding':'gzip, deflate, sdch, br',
                         'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
                         'Cache-Control':'no-cache',
                         'Connection':'keep-alive',
                         'Cookie':'user_trace_token=20170206095738-5dc06777874a41bb8b29cf4d39646b0a; LGUID=20170206095738-a2cd58e2-ec0f-11e6-9af6-525400f775ce; index_location_city=%E5%8C%97%E4%BA%AC; JSESSIONID=BE88414CFBC99C31BA310EFBFD187882; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F112405.html; _gat=1; TG-TRACK-CODE=gongsi_banner; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486346258,1486696551; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1487126212; _ga=GA1.2.509504603.1486346258; LGSID=20170215102426-df16646d-f325-11e6-b05e-525400f775ce; LGRID=20170215103649-99c5efbe-f327-11e6-b063-525400f775ce',
                         'Host':'www.lagou.com',
                         'Pragma':'no-cache',
                         'Referer':'https://www.lagou.com/gongsi/',
                         'Upgrade-Insecure-Requests':1,
                         'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
                         }, 
                     callback=self.parse_model)
            requests.append(request)
        return requests

    def parse_model(self, response):

        if response.status == 404:
            return
        if response.status == 302:
             Request(response._url, 
                    meta={'change_proxy': True},
                    headers={
                         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                         'Accept-Encoding':'gzip, deflate, sdch, br',
                         'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
                         'Cache-Control':'no-cache',
                         'Connection':'keep-alive',
                         'Cookie':'user_trace_token=20170206095738-5dc06777874a41bb8b29cf4d39646b0a; LGUID=20170206095738-a2cd58e2-ec0f-11e6-9af6-525400f775ce; index_location_city=%E5%8C%97%E4%BA%AC; JSESSIONID=BE88414CFBC99C31BA310EFBFD187882; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F112405.html; _gat=1; TG-TRACK-CODE=gongsi_banner; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486346258,1486696551; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1487126212; _ga=GA1.2.509504603.1486346258; LGSID=20170215102426-df16646d-f325-11e6-b05e-525400f775ce; LGRID=20170215103649-99c5efbe-f327-11e6-b063-525400f775ce',
                         'Host':'www.lagou.com',
                         'Pragma':'no-cache',
                         'Referer':'https://www.lagou.com/gongsi/',
                         'Upgrade-Insecure-Requests':1,
                         'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
                         }, 
                     callback=self.parse_model)
        else :

            companys = []
            company =  CommpanyItem()

            selector = Selector(response)
            identification = selector.xpath('//div[@class="company_info"]//a[@class="identification"]/span/text()').extract()
            if len(identification[0]) > 4:
                return

            company['lagou_url'] = response._url
            company['name'] = selector.xpath('//div[@class="company_info"]//h1/a/@title').extract()
            company['short_name'] = selector.xpath('//div[@class="company_info"]//h1/a/text()').extract()
            company['identification'] = 1 if len(identification[0]) == 4 else 0
            company['company_word'] = selector.xpath('//div[@class="company_info"]//div[@class="company_word"]/text()').extract()
            company['href'] = selector.xpath('//div[@class="company_info"]//h1/a/@href').extract()
            company['address'] = selector.xpath('//div[@id="location_container"]//ul/li/p[@class="mlist_li_desc"]/text()').extract()
            companys.append(company)

            return companys 



