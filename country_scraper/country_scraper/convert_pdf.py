import os
from itemadapter import ItemAdapter
from scrapy.pipelines.images import FilesPipeline
from country_scraper.items import CountryScraperItem, CSVItem, RtffilesItem
from pdf2docx import Converter

def convert_pdf(item, file):
    cv = Converter(os.getcwd() + '/' + f"docs/{item['country']}" + "/" + file)
    cv.convert(os.getcwd() + '/' + f"docs/{item['country']}" + "/" + file[:-4] +'.docx', start=0, end=None)
    cv.close()

    # print(item['country'])