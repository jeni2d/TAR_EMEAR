# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class FranceSpider(scrapy.Spider):

    name = 'france'
    # download_delay = 10.0 
    allowed_domains = ['legifrance.gouv.fr']
    # start_urls = ['https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006074228/LEGISCTA000006143855']

    def start_requests(self):
        url = 'https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006074228/LEGISCTA000006143855/#LEGISCTA000006143855'

        yield SeleniumRequest(url=url,
                            callback=self.parse,
                            wait_time=10,
                            wait_until=EC.element_to_be_clickable((By.XPATH, "//div[@class='summary-header print-invisible']"))
            )

    def parse(self, response):
        # print(response.xpath("//div[@class='summary-header print-invisible']/a/text()").get())
        articles = response.xpath("//div[@class='page-content']//article")
        for i in articles:
            title = i.xpath(".//p[@class='name-article' or @class='name-article abrogated']//text()").get().strip()
            date = i.xpath(".//p[@class='date']//text()").get()
            if date:
                date = date.split('du')[1].split('-')[0].strip()
            else:
                date = ''
            text_new = []
            text = i.xpath(".//div[@class='content' or @class='content content-abrogated']//text()").extract()
            for j in text:
                if len(j.strip()) > 1:
                    text_new.append(j.replace('\n', '').replace('  ', '').strip())

            item = CSVItem()
            item['title'] = title
            item['date'] = date
            item['text'] = text_new
            item['url'] = 'https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006074228/LEGISCTA000006143855/#LEGISCTA000006143855'
            item['file_name'] = 'france'
            item['country'] = 'France'
            yield item