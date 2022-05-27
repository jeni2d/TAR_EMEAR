# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
import json
from country_scraper.items import CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class LatviaSpider(scrapy.Spider):

    name = 'latvia1'
    # download_delay = 10.0 
    allowed_domains = ['likumi.lv']
    start_urls = ['https://likumi.lv/ta/id/208072-noteikumi-par-lielgabarita-un-smagsvara-parvadajumiem']
    custom_settings = {
    'ROBOTSTXT_OBEY': False
    } 

    def parse(self, response): 
        date = response.xpath("//div[@id='ver_date']//text()").get()
        date_obj = json.loads(date)['selected']['value']
        block = response.xpath("//div[@class='doc-body']//p")
        print(block)
        for ind, i in enumerate(block):
            text_new = []
            text = i.xpath(".//text()").extract()
            for j in text:
                    if len(j.strip()) > 1:
                        text_new.append(j.replace('\n', '').replace('  ', '').strip())

            if text_new:
                item = CSVItem()
                item['title'] = str(ind) + '_Lat'
                item['date'] = date_obj
                item['text'] = text_new
                item['url'] = 'https://likumi.lv/ta/id/208072-noteikumi-par-lielgabarita-un-smagsvara-parvadajumiem'
                item['file_name'] = 'rules_for_bulk_and_heavy_goods_vehicles'
                item['country'] = 'Latvia'
                yield item