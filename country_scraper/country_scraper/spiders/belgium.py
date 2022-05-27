# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class BelgiumSpider(scrapy.Spider):

    name = 'belgium'
    # download_delay = 10.0 
    allowed_domains = ['wegcode.be']
    start_urls = ['https://wegcode.be/actueel/52-kb/kb-150368/309-art32bisc']

    def parse(self, response):
        # print(response.xpath("//div[@class='content clearfix']//text()").extract())
      
        title = response.xpath("//h1[@class='title']/text()").get()
        date = response.xpath("//p[@class='meta']/time/text()").get()
        text = response.xpath("//div[@class='content clearfix']//text()").extract()
        text_new = []
        for i in text:
            if not re.search('(\n|\t)', i) and len(i.strip()) > 1:
                text_new.append(i.strip())
        item = CSVItem()
        item['title'] = title
        item['date'] = date
        item['text'] = text_new
        item['url'] = 'https://wegcode.be/actueel/52-kb/kb-150368/309-art32bisc'
        item['file_name'] = 'belgium'
        item['country'] = 'Belgium'
        yield item