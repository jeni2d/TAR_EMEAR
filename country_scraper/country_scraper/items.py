# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

#This item is for sites where documents store in files
class CountryScraperItem(scrapy.Item):
    id = scrapy.Field()
    country = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    doc_name = scrapy.Field()

#This item is for files that should be downloaded
class RtffilesItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field
    country = scrapy.Field()

#This item is for sites where documents store on webpages themself
class CSVItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    text = scrapy.Field()
    text_diff = scrapy.Field()
    url = scrapy.Field()
    file_name = scrapy.Field()
    country = scrapy.Field()