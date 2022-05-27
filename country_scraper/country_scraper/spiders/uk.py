# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class UKSpider(scrapy.Spider):

    name = 'uk'
    # download_delay = 10.0 
    allowed_domains = ['gov.uk']
    start_urls = ['https://www.gov.uk/guidance/the-highway-code']
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
        date = response.xpath("//div[@class='gem-c-metadata gem-c-metadata--inverse']//dd[@class='gem-c-metadata__definition' and preceding-sibling::dt[text() = 'Updated:']]/time/text()").get()
        # print(date)

        links = response.xpath("//li[@class='gem-c-document-list__item  ']/a")
        for i in links:
            link = i.xpath("@href").get()
            full_url = response.urljoin(link)
            yield scrapy.Request(
                    url = full_url,
                    method='GET',
                    callback=self.parse_page,
                    cb_kwargs=dict(date=date)

            )

    def parse_page(self, response, date):
        topics = response.xpath("//div[@class='govuk-accordion__section']")
        for i in topics:
            text_new = []
            title = i.xpath(".//h2//text()").get()
            text_new = []
            text = i.xpath(".//div[@class='gem-c-govspeak govuk-govspeak ']//text()").extract()
            for j in text:
                if len(j.strip()) > 1:
                    text_new.append(j.replace('\n', '').replace('  ', '').strip())
            if text_new:
                item = CSVItem()
                item['title'] = title
                item['date'] = date
                item['text'] = text_new
                item['url'] = response.url
                item['file_name'] = 'uk_highway_code'
                item['country'] = 'UK'
                yield item
    
        