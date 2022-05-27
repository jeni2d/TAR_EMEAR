# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class CroatiaSpider(scrapy.Spider):

    name = 'croatia'
    # download_delay = 10.0 
    allowed_domains = ['zakon.hr']
    start_urls = ['https://www.zakon.hr/z/78/Zakon-o-sigurnosti-prometa-na-cestama']
    # custom_settings = {
    # 'ROBOTSTXT_OBEY': False
    # } 
    # def start_requests(self):
    #     url = 'https://www.gov.uk/guidance/the-highway-code/introduction'
    #     yield scrapy.Request(
    #             url=url, 
    #                 method='GET',
    #                 callback=self.parse,
    #                 headers={'User-Agent':'*'}
    #             )

    def parse(self, response): 
        date = response.xpath("//div[@role='naslov-zakona']/p[contains(text(), 'na snazi')]/text()").get().split('od')[1].strip()
        
        print(date)
        textall = response.xpath("//div[@class='tekst-zakona']/p")
        for ind, i in enumerate(textall):
            text_new = []
            text = i.xpath(".//text()").extract()
            for j in text:
                    if len(j.strip()) > 1:
                        text_new.append(j.replace('\n', '').replace('  ', '').strip())

            if text_new:
                item = CSVItem()
                item['title'] = str(ind) + '_Crt'
                item['date'] = date
                item['text'] = text_new
                item['url'] = 'https://www.zakon.hr/z/78/Zakon-o-sigurnosti-prometa-na-cestama'
                item['file_name'] = 'road_traffic_safety_act'
                item['country'] = 'Croatia'
                yield item
        