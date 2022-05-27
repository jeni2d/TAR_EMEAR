# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class CzechSpider(scrapy.Spider):

    name = 'czech'
    # download_delay = 10.0 
    allowed_domains = ['zakonyprolidi.cz']
    start_urls = ['https://www.zakonyprolidi.cz/hledani?text=Vyhl%C3%A1%C5%A1ka%20o%20hmotnostech%2C%20rozm%C4%9Brech%20a%20spojitelnosti%20vozidel']
    custom_settings = {
    'ROBOTSTXT_OBEY': False
    } 

    def parse(self, response): 
        link = response.xpath("//div[@class='Item Doc']/a/@href").get()
        full_url = response.urljoin(link)

        yield scrapy.Request(
                    url=full_url, 
                    method='GET',
                    callback=self.parse_doc
                )
    def parse_doc(self, response):
        
        date = response.xpath("//div[@class='doc-meta']//tr[td[text()='Platnost od']]/td[@class='td1']/span/text()").get()

        block = response.xpath("//div[@class='Frags']/p")
        for ind, i in enumerate(block):
            title = i.xpath("a/@id").get()
            text_new = []
            text = i.xpath(".//text()").extract()
            for j in text:
                    if len(j.strip()) > 1:
                        text_new.append(j.replace('\n', '').replace('  ', '').strip())

            if text_new:
                item = CSVItem()
                item['title'] = title
                item['date'] = date
                item['text'] = text_new
                item['url'] = response.url
                item['file_name'] = 'law_truck_regulations'
                item['country'] = 'Czech'
                yield item