# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from deep_translator import GoogleTranslator


class IrelandSpider(scrapy.Spider):

    name = 'ireland3'
    allowed_domains = ['citizensinformation.ie']
    start_urls = ['https://www.citizensinformation.ie/en/travel_and_recreation/roads_and_safety/road_traffic_speed_limits_in_ireland.html']

    def parse(self, response):

        date = response.xpath("//div[@id='lastupdated']//em").get().split('</b>')[1].replace('</em>', '').strip()
        title = response.xpath("//h1/text()").get()
        for ind, i in enumerate(response.xpath("//div[@class='topic']/div")):
            text_new = []
            text = i.xpath(".//*[self::h2 or self::p]//text()").extract()
            for j in text:
                if len(j.strip()) > 1:
                    text_new.append(j.replace('\n', '').strip())


            if text_new:
                item = CSVItem()
                item['title'] = str(ind) + '_' + title
                item['date'] = date
                item['text'] = text_new
                item['url'] = 'https://www.citizensinformation.ie/en/travel_and_recreation/roads_and_safety/road_traffic_speed_limits_in_ireland.html'
                item['file_name'] = 'ireland'
                item['country'] = 'Ireland'
                yield item
        
        

