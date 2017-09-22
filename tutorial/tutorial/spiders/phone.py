# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from ..items import PhoneDetailItem


class PhonesSpider(scrapy.Spider):
    name = 'phone_spider'

    def __init__(self): 
        '''
        init url and domain
        '''
        super(PhonesSpider, self).__init__()
        self.start_urls = ['https://mobile.zol.com.cn/manu_list.html']
        self.allowed_domain = 'mobile.zol.com.cn'
        self.base_url = 'https://mobile.zol.com.cn{0}'

    def parse(self, response):
        '''
        1.parse brand url
        2.send url to pasre_phone_category
        '''
        div = response.xpath('//body/div[contains(@class, "wrapper clearfix mainMt")]')
        ul = div.xpath('.//ul[contains(@class,"brandsTxt clearfix")]')
        brand_list = ul.xpath('.//li')
        for brand in brand_list:
            _brand = brand.xpath('.//a/text()').extract()[0]
            url = brand.xpath('.//@href').extract()[0]
            yield scrapy.Request(self.base_url.format(url),
                    meta={'brand': _brand},
                    dont_filter=True, callback=self.parse_phone_category)

    def parse_phone_category(self, response):
        '''
        parse brand and it's category
        '''
        brand = response.meta['brand']
        detail_lt = response.xpath('//ul[contains(@class, "timeline-products clearfix")]')
        for categorys in detail_lt:
            ctg_lt = categorys.xpath('.//li')
            for ctg in ctg_lt:
                item = PhoneDetailItem() 
                item['brand'] = brand
                a_tag = ctg.xpath('.//a')[1]
                item['detail'] = a_tag.xpath('.//@href').extract()[0]
                item['category'] = a_tag.xpath('.//text()').extract()[0]
                p_tag = ctg.xpath('.//p')[0]
                item['price'] = p_tag.xpath('.//em/text()').extract()[0]
                yield item




