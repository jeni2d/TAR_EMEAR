# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class SwedenSpider(scrapy.Spider):

    name = 'sweden'
    # download_delay = 10.0 
    allowed_domains = ['riksdagen.se']
    start_urls = ['https://www.riksdagen.se/sv/dokument-lagar/dokument/svensk-forfattningssamling/trafikforordning-19981276_sfs-1998-1276']
    # custom_settings = {
    # 'ROBOTSTXT_OBEY': False
    # } 


    def parse(self, response): 
        # print(response.request.meta)
        # print(response.url)
        date = response.xpath("//section[@class='component-document-summary']/b[text()='Ändrad']/following-sibling::text()").get().split('SFS')[1].strip()


        articles = response.xpath("//section[@class='component-document-summary']/div[2]/*[self::p or self:: pre]")

        for ind, i in enumerate(articles):

            text_new = []
            text = i.xpath(".//text()").extract()
            for j in text:
                if len(j.strip()) > 1:
                    text_new.append(j.replace('\n', '').replace('  ', '').strip())

            if text_new:
                item = CSVItem()
                item['title'] = str(ind) + '_sw'
                item['date'] = date
                item['text'] = text_new
                item['url'] = 'https://www.riksdagen.se/sv/dokument-lagar/dokument/svensk-forfattningssamling/trafikforordning-19981276_sfs-1998-1276'
                item['file_name'] = 'sweden'
                item['country'] = 'Sweden'
                yield item
    
        