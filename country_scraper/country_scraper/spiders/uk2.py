# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CountryScraperItem, RtffilesItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class UKSpider(scrapy.Spider):

    name = 'uk2'
    # download_delay = 10.0 
    allowed_domains = ['gov.gg']
    start_urls = ['https://gov.gg/article/170960/A-Highway-Code-for-Guernsey']
    custom_settings = {
    'ROBOTSTXT_OBEY': False
    } 
    # def start_requests(self):
    #     url = 'https://www.gov.uk/guidance/the-highway-code/introduction'
    #     yield scrapy.Request(
    #             url=url, 
    #                 method='GET',
    #                 callback=self.parse,
    #                 headers={'User-Agent':'*'}
    #             )

    def parse(self, response): 
        date = response.xpath("//p[@id='newsDate']/text()").get().strip()
        text_new = []
        
        item = CountryScraperItem()
        item['country'] = 'UK'
        item['date'] = date
        item['url'] = 'https://gov.gg/article/170960/A-Highway-Code-for-Guernsey'
        item['doc_name'] = 'Guernsey Highway Code'
        yield item

        if CountryScraperPipeline.change == 1:
            link = response.xpath("//div[@id='content']//p[a/text()='The Highway Code for Guernsey']/a/@href").get()
            file_url = response.urljoin(link)
            item = RtffilesItem()
            item['file_urls'] = [file_url]
            item['country'] = 'UK'
            yield item  

  