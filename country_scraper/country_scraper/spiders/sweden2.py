# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CountryScraperItem, RtffilesItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class SwedenSpider(scrapy.Spider):

    name = 'sweden2'
    # download_delay = 10.0 
    allowed_domains = ['transportstyrelsen.se']
    start_urls = ['https://www.transportstyrelsen.se/sv/publikationer-och-rapporter/behallare-dolda-publikationer/publi-vagtrafik/yrkestrafik/Lasta-lagligt1/']
    # custom_settings = {
    # 'ROBOTSTXT_OBEY': False
    # } 


    def parse(self, response): 
        title = response.xpath("//div[@class='media col-xs-12'][.//h3[@aria-label='Legal loading']]/div[@class='media-body']/h3/a/text()").get().strip()
        date = response.xpath("//div[@class='media col-xs-12'][.//h3[@aria-label='Legal loading']]/div[@class='media-body']/p[@class='small']/span/following-sibling::text()").get().replace('.', '').replace('Utgiven ', '').strip()
        link = response.xpath("//div[@class='media col-xs-12'][.//h3[@aria-label='Legal loading']]/div[@class='media-body']/h3/a/@href").get()
        full_url = response.urljoin(link)
        yield scrapy.Request(
                        url=full_url,
                        callback=self.parse_page,
                        cb_kwargs=dict(title=title, date=date)
                    )


    def parse_page(self, response, title, date):
        item = CountryScraperItem()
        item['country'] = 'Sweden'
        item['date'] = date
        item['url'] = response.url
        item['doc_name'] = title
        yield item

        link = response.xpath("//a[@class='btn btn-sm btn-primary ladda-button downloadbutton']/@href").get()
        file_url = response.urljoin(link)

        if CountryScraperPipeline.change == 1:
            yield scrapy.Request(
                        url=file_url,
                        callback=self.parse_link
            )


    def parse_link(self, response):
        item = RtffilesItem()
        item['file_urls'] = [response.url]
        item['country'] = 'Sweden'
        yield item