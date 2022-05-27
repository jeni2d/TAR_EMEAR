# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy_splash import SplashRequest
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CSVItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from seleniumwire import webdriver

class SwissSpider(scrapy.Spider):
    name = 'swiss'
    # download_delay = 10.0 
    allowed_domains = ['fedlex.admin.ch']
    # start_urls = ['https://fedlex.data.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/1962/1364_1409_1420/20220401/de/html/fedlex-data-admin-ch-eli-cc-1962-1364_1409_1420-20220401-de-html.html']
    custom_settings = {
    'ROBOTSTXT_OBEY': False
    } 

    def start_requests(self):
        url = 'https://www.fedlex.admin.ch/eli/cc/1962/1364_1409_1420/de'
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # WEBDRIVER_PATH = r'c:\job\python\chromedriver\chromedriver.exe'
        # driver = webdriver.Chrome(WEBDRIVER_PATH, options=chrome_options) 
        # driver.get(url)
        # url2 = []
        # for request in driver.requests:
        #     request = driver.wait_for_request('admin-ch-eli-cc-1962-1364_1409_1420')
        #     if request.response:
        #         url2.append(request.url)
        #         break
        # driver.quit() 

        # yield scrapy.Request(
        #         url=url2[0], 
        #         method='GET',
        #         callback=self.parse
        #         )
        yield SeleniumRequest(url=url,
                            callback=self.parse,
                            wait_time=10,
                            wait_until=EC.element_to_be_clickable((By.XPATH, "//h1[@class='erlasstitel']"))
            )

        

    def parse(self, response): 
        # print(response.xpath("//main[@id='maintext']//article//p//text()").getall())
        # print(response.xpath("//h1[@class='erlasstitel']//text()").get())

        # date = response.url.split('1420-')[1].split('-')[0].strip()
        date = response.xpath("//tr[@class='page0 visible' and td/span[@class='circle soft-green']]/td[@class='no-padding-right is-active']/text()").get().strip()
        # print(date)

        articles = response.xpath("//main[@id='maintext']//article")

        
        for ind, i in enumerate(articles):
            title = '_'.join(i.xpath("h6/a//text()").extract())
            text_new = []
            text = i.xpath(".//p//text()").extract()
            for j in text:
                if len(j.strip()) > 1:
                    text_new.append(j.replace('\n', '').replace('  ', '').strip())

            if text_new:
                item = CSVItem()
                item['title'] = title
                item['date'] = date
                item['text'] = text_new
                item['url'] = 'https://www.fedlex.admin.ch/eli/cc/1962/1364_1409_1420/de'
                item['file_name'] = 'traffic_regulations_and_vehicle_dimensions'
                item['country'] = 'Swiss'
                yield item
    
        