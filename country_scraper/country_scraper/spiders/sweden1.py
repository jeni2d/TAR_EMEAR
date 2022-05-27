# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CountryScraperItem, RtffilesItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class SwedenSpider(scrapy.Spider):

    name = 'sweden1'
    # download_delay = 10.0 
    allowed_domains = ['transportstyrelsen.se']
    start_urls = ['https://www.transportstyrelsen.se/sv/vagtrafik/Trafikregler/Generella-trafikregler/Hastighet/']
    # custom_settings = {
    # 'ROBOTSTXT_OBEY': False
    # } 


    def parse(self, response): 
        # print(response.request.meta)
        # print(response.url)
        date = response.xpath("//span[@title='Senast ändrad']/span[2]/text()").get().split(':')[1].split(',')[0].strip()



        item = CountryScraperItem()
        item['country'] = 'Sweden'
        item['date'] = date
        item['url'] = 'https://www.transportstyrelsen.se/sv/vagtrafik/Trafikregler/Generella-trafikregler/Hastighet/'
        item['doc_name'] = 'speed table'
        yield item

        if CountryScraperPipeline.change == 1:
            link = response.xpath("//div[@class='list-group-item']/a/@href").get()
            file_url = response.urljoin(link)
            item = RtffilesItem()
            item['file_urls'] = [file_url]
            item['country'] = 'Sweden'
            yield item