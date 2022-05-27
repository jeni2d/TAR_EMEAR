# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CountryScraperItem, RtffilesItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class AustriaSpider(scrapy.Spider):

    name = 'austria2'
    allowed_domains = ['ris.bka.gv.at']
    start_urls = ['https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=Bundesnormen&Gesetzesnummer=10011336']

    def parse(self, response):
        versions_list = []
        for i in response.xpath("//div[@class='contentBlock']/p/a"):
            # link = i.xpath('@href').get()
            text = i.xpath('text()').get()
            # if link.startswith('/eli/bgbl/II'):
            # print(link,':::', text)
            version = re.search('\d+/\d+', text)
            if version:
                versions_list.append((int(version.group(0).split('/')[0]), int(version.group(0).split('/')[1])))
        versions_list = set(versions_list)
        current_version = '/'.join([str(i) for i in max(versions_list, key=lambda x: (x[1], x[0]))])
        # print(versions_list)


        item = CountryScraperItem()
        item['country'] = 'Austria'
        item['date'] = current_version
        item['url'] = 'https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=Bundesnormen&Gesetzesnummer=10011336'
        item['doc_name'] = 'traffic regulations'
        yield item
        
        if CountryScraperPipeline.change == 1:
            for i in response.xpath("//div[@class='FloatRight']//a"):
                # link = i.extract()
                link = i.xpath('@href').get()
                file_url = response.urljoin(link)
                print(file_url)
                name_link = link.split("/")[-1]
                # print(name_link)
                if link.endswith('rtf'):
                    item = RtffilesItem()
                    item['file_urls'] = [file_url]
                    item['country'] = 'Austria'
                    yield item





'''to_translate = 'März'
translated = GoogleTranslator(source='auto', target='en').translate(to_translate)
print(translated)'''
        
                    