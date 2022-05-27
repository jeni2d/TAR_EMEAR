# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CountryScraperItem, RtffilesItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class GreeceSpider(scrapy.Spider):

    name = 'greece'
    # download_delay = 10.0 
    allowed_domains = ['ofae.gr']
    start_urls = ['https://ofae.gr/el/nomothesia/odigies-ee/megista-epitrepomena-vari-diastaseis-oximaton/']
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
        date = re.search('\d{1,2}/\d{1,2}/\d\d\d\d', response.xpath("//section[@class='sidebar-page-body']/p[2]/text()").get()).group(0)
        link = response.xpath("//ul[@class='documents']/li[1]/a//@href").get()
        item = CountryScraperItem()
        item['country'] = 'Greece'
        item['date'] = date
        item['url'] = 'https://ofae.gr/el/nomothesia/odigies-ee/megista-epitrepomena-vari-diastaseis-oximaton/'
        item['doc_name'] = 'Weights and dimensions'
        yield item

        if CountryScraperPipeline.change == 1:
            link = response.xpath("//ul[@class='documents']/li[1]/a//@href").get()
            file_url = response.urljoin(link)
            item = RtffilesItem()
            item['file_urls'] = [file_url]
            item['country'] = 'Greece'
            yield item  

  