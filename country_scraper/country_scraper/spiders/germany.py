# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class GermanySpider(scrapy.Spider):

    name = 'germany'
    # download_delay = 10.0 
    allowed_domains = ['gesetze-im-internet.de']
    # start_urls = ['https://www.gesetze-im-internet.de/stvzo_2012/__32.html', 'https://www.gesetze-im-internet.de/stvzo_2012/__34.html', 'http://www.gesetze-im-internet.de/stvo_2013/__3.html', 'http://www.gesetze-im-internet.de/stvo_2013/__30.html']


    def start_requests(self):
        urls = ['https://www.gesetze-im-internet.de/stvzo_2012/__32.html', 'https://www.gesetze-im-internet.de/stvzo_2012/__34.html', 'http://www.gesetze-im-internet.de/stvo_2013/__3.html', 'http://www.gesetze-im-internet.de/stvo_2013/__30.html']
        
        for index, i in enumerate(urls):
            yield scrapy.Request(
                    url=i, 
                    method='GET',
                    callback=self.parse,
                    cb_kwargs=dict(index=index, url=i)
            )


    def parse(self, response, index, url): 
        # print(response.request.meta)
        # print(response.url)

        '''text_new = []
        text = response.xpath("//div[@class='jnhtml']//text()").extract()
        title = ''.join(response.xpath("//h1//text()").getall()).strip() 
        for j in text:
            if not re.search('(\n|\t)', j) and len(j.strip()) > 1:
                text_new.append(j.strip())
        
        item = CSVItem()
        item['title'] = title
        item['text'] = text_new
        item['url'] = response.url
        item['file_name'] = 'germany'+
        item['country'] = 'Germany'
        yield item'''
        title = ''.join(response.xpath("//h1//text()").getall()).strip() 
        text_all = response.xpath("//div[@class='jnhtml']/div/div[@class='jurAbsatz']")
        for ind, i in enumerate(text_all):
            text_new = []
            text = i.xpath(".//text()").extract()

            for j in text:
                if not re.search('(\n|\t)', j) and len(j.strip()) > 1:
                    text_new.append(j.strip())

            # print(text_new)        
            
            item = CSVItem()
            item['title'] = str(ind) + '_' + title
            item['text'] = text_new
            item['url'] = url
            item['file_name'] = 'germany'+ str(index)
            item['country'] = 'Germany'
            yield item

        