# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class CroatiaSpider(scrapy.Spider):

    name = 'croatia1'
    # download_delay = 10.0 
    allowed_domains = ['narodne-novine.nn.hr']
    start_urls = ['https://narodne-novine.nn.hr/search.aspx?upit=PRAVILNIK++O+PROMETNIM+ZNAKOVIMA%2c+SIGNALIZACIJI+I+OPREMI+NA+CESTAMA&naslovi=da&sortiraj=1&kategorija=1&rpp=10&qtype=3&pretraga=da']
    custom_settings = {
    'ROBOTSTXT_OBEY': False
    } 

    def parse(self, response): 
        date = response.xpath("//div[@class='searchListItem'][1]//div[@class='official-number-and-date']/text()").get().split(',')[-1].strip()
        link = response.xpath("//div[@class='searchListItem'][1]//div[@class='resultTitle']/a/@href").get()
        full_url = response.urljoin(link)


        yield scrapy.Request(
                    url=full_url, 
                    method='GET',
                    callback=self.parse_doc,
                    cb_kwargs=dict(date=date)
                )
    def parse_doc(self, response, date):
        
        block = response.xpath("//div[@class='doc']/div")

        for ind, i in enumerate(block):
            text_new = []
            text = i.xpath("p//text()").extract()
            table = i.xpath("table//tr")
            for j in table:
                    text_new.append(' '.join(j.xpath(".//text()").extract()).replace('\n', '').replace('  ', '').strip())
            for j in text:
                    if len(j.strip()) > 1:
                        text_new.append(j.replace('\n', '').replace('  ', '').strip())

            if text_new:
                item = CSVItem()
                item['title'] = str(ind) + '_Crt'
                item['date'] = date
                item['text'] = text_new
                item['url'] = response.url
                item['file_name'] = 'traffic_signs_signaling_road_equipment'
                item['country'] = 'Croatia'
                yield item