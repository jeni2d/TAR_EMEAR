# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator


class NetherlandsSpider(scrapy.Spider):

    name = 'netherlands1'
    # download_delay = 10.0 
    allowed_domains = ['overheid.nl']
    start_urls = ['https://wetten.overheid.nl/BWBR0004825']


    def parse(self, response): 
        # print(response.request.meta)
        # print(response.url)
        date_raw = response.xpath("//div[@id='regeling']/div[@class='article__header--law article__header--main']/p/br/following-sibling::text()").get()
        date = re.search('\d\d-\d\d-\d\d\d\d', date_raw).group(0)


        articles1 = response.xpath("//div[@class='wet-besluit']/div[@class='wettekst']//div[@class='artikel']")
        for ind, i in enumerate(articles1):
            title = i.xpath("@id").get().split('_')[-1]
            text_new = []
            text = i.xpath(".//text()").extract()
            for j in text:
                if len(j.strip()) > 1:
                    text_new.append(j.replace('\n', '').replace('  ', '').strip())

            item = CSVItem()
            item['title'] = str(ind) + '_' + title
            item['date'] = date
            item['text'] = text_new
            item['url'] = response.url
            item['file_name'] = 'netherlands1'
            item['country'] = 'Netherlands'
            yield item

        