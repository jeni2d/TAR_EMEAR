# -*- coding: utf-8 -*-
from os import name
import scrapy
from scrapy.http import Request, HtmlResponse
import re
from country_scraper.items import CountryScraperItem, RtffilesItem
from country_scraper.pipelines import CountryScraperPipeline
from deep_translator import GoogleTranslator
from country_scraper.expand_link_bit import expand_link


class IrelandSpider(scrapy.Spider):

    name = 'ireland1'
    # allowed_domains = ['trafficsigns.ie']
    # start_urls = ['https://www.trafficsigns.ie/tsm-cur']
    start_urls = ['https://dttassupportoffice.sharepoint.com/:b:/s/DTTASSupportOffice/EdPYE2n5frZDoQUIhtRB87IBPw1dTPG5Nt2aRb4yI9vVoQ?e=n26KYb']

    def parse(self, response):
        print('--------')
        print(response.url)
        print('--------')
        print(response.xpath("//button[@type='button']"))

        item = RtffilesItem()
        item['file_urls'] = ['https://dttassupportoffice.sharepoint.com/sites/DTTASSupportOffice/_layouts/15/download.aspx?SourceUrl=%2Fsites%2FDTTASSupportOffice%2FTraffic%20Signs%20ManualTTM%2FWebsite%2FLive%20Documents%20%28newNov21%29%2FChapters%2FChapter%200%20%2D%20Master%20%28November%202021%29%2Epdf']
        item['country'] = 'Ireland'
        yield item



    #     for i in response.xpath("//table[@class='_1zeqi']/tbody/tr"):
    #         doc_name = i.xpath("td[2]//text()").get()
    #         date = i.xpath("td[4]//text()").get()
    #         link = expand_link(i.xpath("td[3]//a/@href").get().replace('https://', ''))

    #         # file_url = response.urljoin(link)

    #         yield scrapy.Request(
    #             url=link,
    #             callback=self.parse_link,
    #             cb_kwargs=dict(doc_name=doc_name, date=date),
    #             headers={'User-Agent':'MS Search 6.0 Robot'}
    #         )

    # def parse_link(self, response, doc_name, date):

    #         item = CountryScraperItem()
    #         item['country'] = 'Ireland'
    #         item['date'] = date
    #         item['url'] = response.url
    #         item['doc_name'] = doc_name
    #         yield item
        
    #         if CountryScraperPipeline.change == 1:
    #             item = RtffilesItem()
    #             item['file_urls'] = [response.url]
    #             item['country'] = 'Ireland'
    #             yield item

