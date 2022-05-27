# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from deep_translator import GoogleTranslator


class AustriaSpider(scrapy.Spider):

    name = 'austria'
    allowed_domains = ['oesterreich.gv.at']
    start_urls = ['https://www.oesterreich.gv.at/themen/freizeit_und_strassenverkehr/kfz.html']

    def parse(self, response):
        for i in response.xpath("//main[@id='content']/ul/li/a/@href")[:-1]:
            # print(i.get())
            full_url = response.urljoin(i.get())
            yield scrapy.Request(
            url=full_url,
            callback=self.parse_tree,
            cb_kwargs=dict(url=full_url)
        )
        # link = response.urljoin(response.xpath("//main[@id='content']/ul/li[16]/a/@href").get())
        '''link = 'https://www.oesterreich.gv.at/themen/freizeit_und_strassenverkehr/kfz/3/1/Seite.061522.html#abholung'
        yield scrapy.Request(
            url=link,
            callback=self.parse_tree
        )'''


    def parse_tree(self, response, url):
        # print(response.xpath("//main[@id='content']/h1/following-sibling::*[position()<=2][self::ul]"))
        if response.xpath("//main[@id='content']/div[@class='toc' or @class='toc toc-multicol']") or not response.xpath("//main[@id='content']/h1/following-sibling::*[position()<=2][self::ul]"):
            date = response.xpath("//div[@class='acceptance']/div[@class='state']/text()").get().split(':')[1].strip()
            title = ''.join(response.xpath("//main[@id='content']/h1//text()").getall()).strip() 
            text = response.xpath("//main[@id='content']//text()").extract()
            text_new = []
            for i in text:
                if not re.search('(\n|\t)', i) and len(i.strip()) > 1:
                    text_new.append(i.strip())

            item = CSVItem()
            item['title'] = title
            item['date'] = date
            item['text'] = text_new
            item['url'] = url
            item['file_name'] = 'austria_traffic'
            item['country'] = 'Austria'
            yield item
        else:
            for i in response.xpath("//main[@id='content']/ul/li"):
                if i.xpath("strong"):
                    pass
                    
                elif i.xpath("ul/li"):
                    for j in i.xpath("ul/li"):
                        full_url = response.urljoin(j.xpath("a/@href").get())
                        yield scrapy.Request(
                            url=full_url,
                            callback=self.parse_page,
                            cb_kwargs=dict(url=full_url)
                        )
                        # print(j.xpath("a/@href").get())

                else:
                    full_url = response.urljoin(i.xpath("a/@href").get())
                    yield scrapy.Request(
                        url=full_url,
                        callback=self.parse_page,
                        cb_kwargs=dict(url=full_url)
                    )
                    # print(i.xpath("a/@href").get())

    def parse_page(self, response, url):
        date = response.xpath("//div[@class='acceptance']/div[@class='state']/text()").get().split(':')[1].strip()
        title = ''.join(response.xpath("//main[@id='content']/h1//text()").getall()).strip() 
        text = response.xpath("//main[@id='content']//text()").extract()
        text_new = []
        for i in text:
            if not re.search('(\n|\t)', i) and len(i.strip()) > 1:
                text_new.append(i.strip())

        item = CSVItem()
        item['title'] = title
        item['date'] = date
        item['text'] = text_new
        item['url'] = url
        item['file_name'] = 'austria_traffic'
        item['country'] = 'Austria'
        yield item




                    