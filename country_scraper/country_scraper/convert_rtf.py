import win32com.client
import os
from itemadapter import ItemAdapter
from scrapy.pipelines.images import FilesPipeline
from country_scraper.items import CountryScraperItem, CSVItem, RtffilesItem



# rootDir = 'c:/job/python/TAR_EMEAR/doc_test/Text1.docx'
# rootDir = 'c:/job/python/TAR_EMEAR/doc_test'

def ConvertRtfToDocx(item, file):
    word = win32com.client.Dispatch("Word.Application")
    wdFormatDocumentDefault = 16
    doc = word.Documents.Open(os.getcwd() + '/' + f"docs/{item['country']}" + "/" + file)
    doc.SaveAs(str(os.getcwd() + '/' + f"docs/{item['country']}" + "/{}.docx".format(file[:-4])), FileFormat=wdFormatDocumentDefault)
    doc.Close()
    word.Quit()
	


# ConvertRtfToDocx(item, 'Text_test.rtf')

