# -*- coding: utf-8 -*-
from os import name
from pydoc import doc
import scrapy
from scrapy.http import Request, HtmlResponse
from country_scraper.items import CountryScraperItem
import datetime


class FinlandSpider(scrapy.Spider):

    name = 'finland'
    allowed_domains = ['finlex.fi']
    start_urls = ['https://www.finlex.fi/fi/laki/smur/2018/20180729']

    def parse(self, response):
        dates = []
        doc_name = response.xpath("//div[@id='document']/h3/text()").get()
        print(doc_name)
        dateurl = response.xpath("//div[@id='muutokset']/ul/li")
        for i in dateurl:
            datetime_object = datetime.datetime.strptime(i.xpath("div[@class='voimaan']/text()").get(), '%d.%m.%Y')
            doc_url = response.urljoin(i.xpath("a[@class='alkup']/@href").get())
            dates.append((datetime_object, doc_url))
        # print(str(max(dates))[:10])
        # print(str(max(dates, key=lambda x: x[0])[0])[:10])
        # print(max(dates, key=lambda x: x[0])[1])

        date = str(max(dates, key=lambda x: x[0])[0])[:10]
        url = max(dates, key=lambda x: x[0])[1]

        item = CountryScraperItem()
        item['country'] = 'Finland'
        item['date'] = date
        item['url'] = url
        item['doc_name'] = doc_name
        yield item