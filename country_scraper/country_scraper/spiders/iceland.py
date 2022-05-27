# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem



class IcelandSpider(scrapy.Spider):

    name = 'iceland'
    download_delay = 5 
    allowed_domains = ['reglugerd.is']
    start_urls = ['https://www.reglugerd.is/reglugerdir/allar/nr/155-2007']

    def start_requests(self):
        url = 'https://www.reglugerd.is/reglugerdir/allar/nr/155-2007'
        yield scrapy.Request(
                url=url, 
                method='GET',
                callback=self.parse,
                headers={'User-Agent':'*'}
                )

    def parse(self, response):
        versions_list = []
        ver = response.xpath("//div[@class='rinfo']/ul/li")
        for i in ver:
            version = i.xpath("span[@class='nr']/text()").get()
            if version:
                versions_list.append((int(version.split('/')[0]), int(version.split('/')[1])))
        current_version = '/'.join([str(i) for i in max(versions_list, key=lambda x: (x[1], x[0]))])

        title = response.xpath("//h1/text()").get()
        text = response.xpath("//div[@class='boxbody']/*[self::p or self::ol]//text()").extract()
        text_new = []
        for i in text:
            if not re.search('(\n|\t)', i) and len(i.strip()) > 1:
                text_new.append(i.strip())
        print(text_new)
        
        item = CSVItem()
        item['title'] = title
        item['date'] = current_version
        item['text'] = text_new
        item['url'] = 'https://www.reglugerd.is/reglugerdir/allar/nr/155-2007'
        item['file_name'] = 'iceland'
        item['country'] = 'Iceland'
        yield item

