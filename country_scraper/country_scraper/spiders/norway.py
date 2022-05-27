# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class NorwaySpider(scrapy.Spider):

    name = 'norway'
    # download_delay = 10.0 
    allowed_domains = ['lovdata.no']
    start_urls = ['https://lovdata.no/dokument/LTI/forskrift/2014-01-15-28']
    custom_settings = {
    'ROBOTSTXT_OBEY': False
    } 


    def parse(self, response): 
        # print(response.request.meta)
        # print(response.url)
        date = response.xpath("//table[@class=' meta']//th[text()='Ikrafttredelse']/following-sibling::td/text()").get()


        articles = response.xpath("//div[@id='documentBody']/div[@data-level='1']")
        for ind, i in enumerate(articles):
            title = i.xpath("h2/text()").get()
            text_new = []
            text = i.xpath(".//p//text()").extract()
            table = i.xpath(".//table//tr")
            for j in table:
                text_new.append(' '.join(j.xpath(".//text()").extract()).strip())
            for j in text:
                if len(j.strip()) > 1:
                    text_new.append(j.replace('\n', '').replace('  ', '').strip())

            item = CSVItem()
            item['title'] = title
            item['date'] = date
            item['text'] = text_new
            item['url'] = 'https://lovdata.no/dokument/LTI/forskrift/2014-01-15-28'
            item['file_name'] = 'norway'
            item['country'] = 'Norway'
            yield item

        