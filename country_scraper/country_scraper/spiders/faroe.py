# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class FaroeSpider(scrapy.Spider):

    name = 'faroe'
    # download_delay = 10.0 
    allowed_domains = ['logir.fo']
    start_urls = ['https://www.logir.fo/Logtingslogarkunngerd/14-fra-02-03-1988-um-ferdslu-sum-seinast-broytt-vid-logtingslog-nr-49-fra-11']

    def parse(self, response):
        # print(response.xpath("//div[@class='content clearfix']//text()").extract())


        titledate = response.xpath("//h1[@class='mb-big']/text()").get()
        title = titledate.split('løgtingslóg nr.')[0].strip()
        date = titledate.split('løgtingslóg nr.')[1].strip()
        text = response.xpath("//div[@class='WordSection1']//text()").extract()
        text_new = []
        for i in text:
            if not re.search('(\n|\t)', i) and len(i.strip()) > 1:
                text_new.append(i.strip())
        # print(text_new)
        item = CSVItem()
        item['title'] = title
        item['date'] = date
        item['text'] = text_new
        item['url'] = 'https://www.logir.fo/Logtingslogarkunngerd/14-fra-02-03-1988-um-ferdslu-sum-seinast-broytt-vid-logtingslog-nr-49-fra-11'
        item['file_name'] = 'faroe'
        item['country'] = 'Faroe'
        yield item