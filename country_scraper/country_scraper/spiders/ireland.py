# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CountryScraperItem, RtffilesItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class IrelandSpider(scrapy.Spider):

    name = 'ireland'
    allowed_domains = ['rsa.ie']
    start_urls = ['https://www.rsa.ie/road-safety/road-users/professional-drivers/vehicle-safety-legislation/weights-and-dimensions']

    def parse(self, response):

        date = response.xpath("//a[@class='download-link']//span[@class='title']/text()").get().split(' - ')[1].strip()
        # for i in response.xpath("//a[@class='download-link']"):
            # print(i.xpath(".//span[@class='title']@href").get())
            
        # link = response.xpath("//a[@class='download-link']/@href").get().split('?')[0]
        # link = response.xpath("//tr//a[text()='1960.03.15.pdf']/@href").get()
        # file_url = response.urljoin(link)
        # print(date)


        item = CountryScraperItem()
        item['country'] = 'Ireland'
        item['date'] = date
        item['url'] = 'https://www.rsa.ie/road-safety/road-users/professional-drivers/vehicle-safety-legislation/weights-and-dimensions'
        item['doc_name'] = 'Weights and Dimensions'
        yield item
        
        if CountryScraperPipeline.change == 1:
            for i in response.xpath("//a[@class='download-link']"):
                link = i.xpath("@href").get().split('?')[0]
                file_url = response.urljoin(link)
                item = RtffilesItem()
                item['file_urls'] = [file_url]
                item['country'] = 'Ireland'
                yield item

