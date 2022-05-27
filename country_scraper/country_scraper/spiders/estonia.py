# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class EstoniaSpider(scrapy.Spider):

    name = 'estonia'
    # download_delay = 10.0 
    allowed_domains = ['riigiteataja.ee']
    start_urls = ['https://www.riigiteataja.ee/otsingu_tulemus.html?sakk=kehtivad&otsisona=Mootors%C3%B5iduki+ja+selle+haagise+tehnon%C3%B5uded+ning+n%C3%B5uded+varustusele']
    custom_settings = {
    'ROBOTSTXT_OBEY': False
    } 

    def parse(self, response): 
        link = response.xpath("//table[@class='data']//td[1]/a/@href").get()
        full_url = response.urljoin(link)
        yield scrapy.Request(
                    url=full_url, 
                    method='GET',
                    callback=self.parse_doc
                )

    def parse_doc(self, response):
        
        date = response.xpath("//table[@class='meta']//tr[th[text()='Redaktsiooni jõustumise kp:']]/td/text()").get()
        block = response.xpath("//div[@id='article-content']//p")
        for ind, i in enumerate(block):
            text_new = []
            text = i.xpath(".//text()").extract()
            for j in text:
                    if len(j.strip()) > 1:
                        text_new.append(j.replace('\n', '').replace('  ', '').strip())

            if text_new:
                item = CSVItem()
                item['title'] = str(ind) + '_Est'
                item['date'] = date
                item['text'] = text_new
                item['url'] = response.url
                item['file_name'] = 'motor_vehicles_and_their_trailers'
                item['country'] = 'Estonia'
                yield item
