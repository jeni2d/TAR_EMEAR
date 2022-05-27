# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CountryScraperItem, RtffilesItem, CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class SwedenSpider(scrapy.Spider):

    name = 'sweden3'
    # download_delay = 10.0 
    allowed_domains = ['transportstyrelsen.se']
    start_urls = ['https://transportstyrelsen.se/sv/vagtrafik/miljo/miljozoner/']
    # custom_settings = {
    # 'ROBOTSTXT_OBEY': False
    # } 


    def parse(self, response): 
        title = response.xpath("//main[@id='huvudinnehall']/h1/text()").get().strip()
        date = response.xpath("//span[@id='pageDate']/span[2]/text()").get().split(':')[1].split(',')[0].strip()
        text = response.xpath("//main[@id='huvudinnehall']//p//text()").extract()
        text_new = []
        for j in text:
                if len(j.strip()) > 1:
                    text_new.append(j.replace('\n', '').replace('  ', '').strip())

        # link = response.xpath("//div[@class='col-xs-12']//div[@class='list-group-item']/a/@href").get()
        # full_url = response.urljoin(link)

        item = CSVItem()
        item['title'] = title
        item['date'] = date
        item['text'] = text_new
        item['url'] = 'https://transportstyrelsen.se/sv/vagtrafik/miljo/miljozoner/'
        item['file_name'] = 'sweden_env_zones'
        item['country'] = 'Sweden'
        yield item
        


        # yield scrapy.Request(
        #                 url=full_url,
        #                 callback=self.parse_page
        #             )


    # def parse_page(self, response):
    #     date = response.xpath("//span[@id='pageDate']/span[2]/text()").get().split(':')[1].split(',')[0].strip()
    #     print(date)

        # item = CountryScraperItem()
        # item['country'] = 'Sweden'
        # item['date'] = date
        # item['url'] = response.url
        # item['doc_name'] = title
        # yield item

        # link = response.xpath("//a[@class='btn btn-sm btn-primary ladda-button downloadbutton']/@href").get()
        # file_url = response.urljoin(link)

        # if CountryScraperPipeline.change == 1:
        #     yield scrapy.Request(
        #                 url=file_url,
        #                 callback=self.parse_link
        #     )


    # def parse_link(self, response):
    #     item = RtffilesItem()
    #     item['file_urls'] = [response.url]
    #     item['country'] = 'Sweden'
    #     yield item