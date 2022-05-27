# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
from scrapy.selector import Selector
import re
import json
from country_scraper.items import CSVItem
# from scrapy_selenium import SeleniumRequest


class DenmarkSpider(scrapy.Spider):

    name = 'denmark'
    # download_delay = 10.0 
    allowed_domains = ['retsinformation.dk']
    start_urls = ['https://www.retsinformation.dk/api/document/185300/references/0']
    # start_urls = ['https://www.retsinformation.dk/api/document/eli/lta/2016/1497']

    '''def parse(self, response):
        data = response.json()
        content = Selector(text = data[0]['documentHtml'])
        title = data[0]['title']
        text = content.xpath("//text()").extract()
        text_new = []
        for i in text:
            if not re.search('(\n|\t)', i) and len(i.strip()) > 1:
                text_new.append(i.strip())
        # print(text_new)
        yield scrapy.Request(
                        url='https://www.retsinformation.dk/api/document/185300/references/0',
                        callback=self.parse_date,
                        cb_kwargs=dict(title=title, text=text_new)
                    )

    def parse_date(self, response, title, text):
        data = response.json()
        date = data['referenceGroups'][0]['references'][-1]['offentliggoerelsesDato']
        
        item = CSVItem()
        item['title'] = title
        item['date'] = date
        item['text'] = text
        item['url'] = 'https://www.retsinformation.dk/eli/lta/2016/1497'
        item['file_name'] = 'denmark'
        item['country'] = 'Denmark'
        yield item'''

    def parse(self, response):
        data = response.json()
        date = data['referenceGroups'][0]['references'][-1]['offentliggoerelsesDato']

        yield scrapy.Request(
                        url='https://www.retsinformation.dk/api/document/eli/lta/2016/1497',
                        callback=self.parse_all,
                        cb_kwargs=dict(date=date)
        )

    def parse_all(self, response, date):
        data = response.json()
        content = Selector(text = data[0]['documentHtml'])
        title = data[0]['title']

        text_all = content.xpath("//body/p")
        for index, i in enumerate(text_all):
            text_new = []
            text = i.xpath(".//text()").extract()
            for j in text:
                if not re.search('(\n|\t)', j) and len(j.strip()) > 1:
                    text_new.append(j.strip())

            item = CSVItem()
            item['title'] = str(index) + '_' + title
            item['date'] = date
            item['text'] = text_new
            item['url'] = 'https://www.retsinformation.dk/eli/lta/2016/1497'
            item['file_name'] = 'denmark'
            item['country'] = 'Denmark'
            yield item

        





                    