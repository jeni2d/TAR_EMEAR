# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CountryScraperItem, RtffilesItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class IrelandSpider(scrapy.Spider):

    name = 'ireland2'
    allowed_domains = ['rsa.ie']
    start_urls = ['https://www.rsa.ie/services/learner-drivers/resources/rules-of-the-road']

    def parse(self, response):

        date = response.xpath("//a[@class='download-link']//span[@class='info']/text()").get().split('|')[1].replace('KB', '').strip()
        # for i in response.xpath("//a[@class='download-link']"):
            # print(i.xpath(".//span[@class='title']@href").get())
            
        # link = response.xpath("//a[@class='download-link']/@href").get().split('?')[0]
        # link = response.xpath("//tr//a[text()='1960.03.15.pdf']/@href").get()
        # file_url = response.urljoin(link)
        print(date)


        item = CountryScraperItem()
        item['country'] = 'Ireland'
        item['date'] = date
        item['url'] = 'https://www.rsa.ie/services/learner-drivers/resources/rules-of-the-road'
        item['doc_name'] = 'Rules of the Road'
        yield item
        
        if CountryScraperPipeline.change == 1:
            link = response.xpath("//a[@class='download-link']/@href").get().split('?')[0]
            file_url = response.urljoin(link)
            item = RtffilesItem()
            item['file_urls'] = [file_url]
            item['country'] = 'Ireland'
            yield item

