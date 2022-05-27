# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class SpainSpider(scrapy.Spider):

    name = 'spain'
    # download_delay = 10.0 
    allowed_domains = ['mitma.gob.es']
    # start_urls = ['https://www.mitma.gob.es/transporte-terrestre/inspeccion-y-seguridad-en-el-transporte/pesos-y-dimensiones/inspeccion-de-los-transportes-por-carretera-pesos-maximos-y-requisitos-de-utilizacion']

    def start_requests(self):
        url = 'https://www.mitma.gob.es/transporte-terrestre/inspeccion-y-seguridad-en-el-transporte/pesos-y-dimensiones/inspeccion-de-los-transportes-por-carretera-pesos-maximos-y-requisitos-de-utilizacion'
        # url = 'https://www.mitma.gob.es/transporte-terrestre/inspeccion-y-seguridad-en-el-transporte/pesos-y-dimensiones/pesos/pesos-remolques'
        yield scrapy.Request(
                url=url, 
                    method='GET',
                    callback=self.parse,
                    headers={'User-Agent':'*'},
                    cb_kwargs=dict(url=url)
                )


    def parse(self, response, url):
        if response.xpath("//div[@class='main_column']//h1/following-sibling::*[position()<=3][self::ul]"):
            for i in response.xpath("//div[@class='main_column']//ul/li/a/@href"):
                # print(i.get())
                full_url = response.urljoin(i.get())
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse,
                    headers={'User-Agent':'*'},
                    cb_kwargs=dict(url=full_url)
                    )
        else:
            title = response.xpath("//div[@class='container_generico']/h1/text()").get()
            text = response.xpath("//div[@class='main_column']//text()").extract()
            text_new = []
            for i in text:
                if not re.search('(\n|\t)', i) and len(i.strip()) > 1:
                    text_new.append(i.strip())
            print(title)
            item = CSVItem()
            item['title'] = title
            item['text'] = text_new
            item['url'] = url
            item['file_name'] = 'spain'
            item['country'] = 'Spain'
            yield item

        





                    