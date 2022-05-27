# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CountryScraperItem, RtffilesItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class ItalySpider(scrapy.Spider):

    name = 'italy'
    allowed_domains = ['pianostrutturale.info']
    # download_delay = 5
    # start_urls = ['http://www.pianostrutturale.info/normativa.html']

    def start_requests(self):
        url = 'http://www.pianostrutturale.info/normativa.html'
        yield scrapy.Request(
                url=url, 
                    method='GET',
                    callback=self.parse,
                    headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                            'Accept-Encoding': 'gzip, deflate',
                            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                    }
                )

    def parse(self, response):

        date = response.xpath("//a[contains(i, 'Regolamento di esecuzione e di attuazione del Nuovo Codice della Strada')]/text()").get().split('D.P.R.')[1].split(',')[0].strip()


        item = CountryScraperItem()
        item['country'] = 'Italy'
        item['date'] = date
        item['url'] = 'http://www.pianostrutturale.info/normativa.html'
        item['doc_name'] = 'Motor vehicle regulations'
        yield item
        
        if CountryScraperPipeline.change == 1:
            link = response.xpath("//a[contains(i, 'Regolamento di esecuzione e di attuazione del Nuovo Codice della Strada')]/@href").get()
            file_url = response.urljoin(link)
            item = RtffilesItem()
            item['file_urls'] = [file_url]
            item['country'] = 'Italy'
            yield item

