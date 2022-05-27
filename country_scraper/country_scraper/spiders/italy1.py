# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CountryScraperItem, RtffilesItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class ItalySpider(scrapy.Spider):

    name = 'italy1'
    allowed_domains = ['certifico.com']
    # download_delay = 5
    start_urls = ['https://www.certifico.com/id/15288']


    def parse(self, response):

        date = response.xpath("//div[@id='system']//table//time/text()").get()
        item = CountryScraperItem()
        item['country'] = 'Italy'
        item['date'] = date
        item['url'] = 'https://www.certifico.com/id/15288'
        item['doc_name'] = 'Traffic regulation Ordinance'
        yield item
        
        if CountryScraperPipeline.change == 1:
            link = response.xpath("//td[@class='at_filename']/a/@href").get()
            file_url = response.urljoin(link+'.pdf')
            item = RtffilesItem()
            item['file_urls'] = [file_url]
            item['country'] = 'Italy'
            yield item

