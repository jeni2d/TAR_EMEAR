# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CountryScraperItem, RtffilesItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator
import datetime

class LuxembourgSpider(scrapy.Spider):

    name = 'luxembourg'
    allowed_domains = ['legilux.public.lu', 'data.legilux.public.lu']
    start_urls = ['https://legilux.public.lu/eli/etat/leg/code/route/20210820']
    custom_settings = {
    'ROBOTSTXT_OBEY': False
    } 

    def parse(self, response):

        dates = []

        for i in response.xpath("//div[@class='panel-body']/ul[@class='list-unstyled']/li"):
            datetime_object = datetime.datetime.strptime(i.xpath("a/text()").get().split('au')[1].strip(), '%d/%m/%Y')
            dates.append(datetime_object)
        
        date = str(max(dates))[:10]
        to_url = date.replace('-', '')

        link = f'https://data.legilux.public.lu/file/eli-etat-leg-code-route-{to_url}-fr-pdf.pdf'
        item = CountryScraperItem()
        item['country'] = 'Luxembourg'
        item['date'] = date
        item['url'] = 'https://legilux.public.lu/eli/etat/leg/code/route/20210820'
        item['doc_name'] = 'full driving legislation'
        yield item
        
        if CountryScraperPipeline.change == 1:
            item = RtffilesItem()
            item['file_urls'] = [link]
            item['country'] = 'Luxembourg'
            yield item

