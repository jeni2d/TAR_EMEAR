# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CountryScraperItem, RtffilesItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class GibraltarSpider(scrapy.Spider):

    name = 'gibraltar'
    allowed_domains = ['gibraltarlaws.gov.gi']
    start_urls = ['https://www.gibraltarlaws.gov.gi/uploads/legislations/traffic/']

    def parse(self, response):
        date = response.xpath("//tr[td/a[text()='1960.03.15.pdf']]/td[@align='right']/text()").get()
        link = response.xpath("//tr//a[text()='1960.03.15.pdf']/@href").get()
        file_url = response.urljoin(link)
        # print(file_url)
        item = CountryScraperItem()
        item['country'] = 'Gibraltar'
        item['date'] = date
        item['url'] = 'https://www.gibraltarlaws.gov.gi/uploads/legislations/traffic/'
        item['doc_name'] = 'traffic regulations'
        yield item
        
        if CountryScraperPipeline.change == 1:
            item = RtffilesItem()
            item['file_urls'] = [file_url]
            item['country'] = 'Gibraltar'
            yield item

