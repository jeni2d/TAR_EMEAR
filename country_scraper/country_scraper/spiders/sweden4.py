# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class SwedenSpider(scrapy.Spider):

    name = 'sweden4'
    # download_delay = 10.0 
    allowed_domains = ['riksdagen.se']
    start_urls = ['https://www.riksdagen.se/sv/dokument-lagar/dokument/svensk-forfattningssamling/lag-2001559-om-vagtrafikdefinitioner_sfs-2001-559']
    # custom_settings = {
    # 'ROBOTSTXT_OBEY': False
    # } 


    def parse(self, response): 
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
                item['title'] = str(ind) + 'sw'
                item['date'] = date
                item['text'] = text_new
                item['url'] = 'https://www.riksdagen.se/sv/dokument-lagar/dokument/svensk-forfattningssamling/lag-2001559-om-vagtrafikdefinitioner_sfs-2001-559'
                item['file_name'] = 'sweden_road_traffic_definitions'
                item['country'] = 'Sweden'
                yield item
    
        