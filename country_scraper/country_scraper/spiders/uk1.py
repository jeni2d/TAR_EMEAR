# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class UKSpider(scrapy.Spider):

    name = 'uk1'
    # download_delay = 10.0 
    allowed_domains = ['gov.uk']
    start_urls = ['https://www.gov.uk/government/publications/hgv-maximum-weights/hgv-maximum-weights']
    custom_settings = {
    'ROBOTSTXT_OBEY': False
    } 
    # def start_requests(self):
    #     url = 'https://www.gov.uk/guidance/the-highway-code/introduction'
    #     yield scrapy.Request(
    #             url=url, 
    #                 method='GET',
    #                 callback=self.parse,
    #                 headers={'User-Agent':'*'}
    #             )

    def parse(self, response): 
        date = response.xpath("//p[@class='publication-header__last-changed']/text()").get().replace('Published', '').strip()
        text_new = []

        text = response.xpath("//div[@class='govspeak']//p//text()").extract()
        table = response.xpath("//div[@class='govspeak']//table//tr")
        for j in table:
                text_new.append(' '.join(j.xpath(".//text()").extract()).replace('\n', '').replace('  ', '').strip())
        for j in text:
                if len(j.strip()) > 1:
                    text_new.append(j.replace('\n', '').replace('  ', '').strip())


        item = CSVItem()
        item['title'] = 'HGV maximum weights'
        item['date'] = date
        item['text'] = text_new
        item['url'] = 'https://www.gov.uk/government/publications/hgv-maximum-weights/hgv-maximum-weights'
        item['file_name'] = 'hgv_maximum_weights'
        item['country'] = 'UK'
        yield item
        