# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# from scrapy.pipelines.images import FilesPipeline
from scrapy.pipelines.files import FilesPipeline
from country_scraper.items import CountryScraperItem, CSVItem, RtffilesItem
from country_scraper.compare_docx import compare_doc
from country_scraper.convert_pdf import convert_pdf
from country_scraper.convert_rtf import ConvertRtfToDocx
from country_scraper.send_notification import send_note
import sqlite3
import pandas as pd
import ast
import datetime
import os

#Pipeline is for sites where documents store in files. This pipeline create records in DB, check changes and update dates  
class CountryScraperPipeline():
    change = 0

    def __init__(self):
        self.create_connection()

    #create DB connection
    def create_connection(self):
        self.conn = sqlite3.connect('c:/job/python/TAR_EMEAR/country_docs_tar.db')
        self.curr = self.conn.cursor()

    #check type of Item
    def process_item(self, item, spider):
        if isinstance(item, CountryScraperItem):
            self.store_item(item)
        return item

    #check whether the item exists and if so, check change in date and if so, update record
    def store_item(self, item): 
        self.curr.execute("SELECT country, date, url, doc_name FROM docs WHERE doc_name = ? AND country = ?;", [item['doc_name'], item['country']])
        res = self.curr.fetchone()
        if res:
            print(res[1])
            print('----------')
            if res[1] != item['date']:
                self.curr.execute("UPDATE docs SET date = ? WHERE url = ? ", [item['date'], item['url']])
                CountryScraperPipeline.change = 1
                self.tracking(item)
        if not res:
            self.curr.execute("""INSERT INTO docs(country, date, url, doc_name) VALUES(?, ?, ?, ?)""", [item['country'], item['date'], item['url'], item['doc_name']])
            CountryScraperPipeline.change = 1
        self.conn.commit()

    #this method update tracking
    def tracking(self, item):
        df = pd.read_csv('docs/tracking.csv', sep=',')
        df = pd.concat([df, pd.DataFrame.from_records([{'Country': item['country'], 'Title': item['doc_name'], 'Date': item['date'], 'Url': item['url']}])])
        df.to_csv('docs/tracking.csv', sep=',', index=False)

#This pipeline is for sites where documents store on webpages themself. Pages will be parsed and downloaded to CSV files and compare if needed
class CSVPipeline():
    def process_item(self, item, spider):
        if isinstance(item, CSVItem):
            try:
                df = pd.read_csv('docs/{}/{}.csv'.format(item['country'], item['file_name']), sep=',')
            except FileNotFoundError:
                with open('docs/{}/{}.csv'.format(item['country'], item['file_name']), 'a', encoding='utf-8') as file:
                    row = 'Title,' + 'Date,' + 'Text,' + 'Text_diff_new,' + 'Text_diff_old' + '\n'
                    file.write(row)
            finally:
                df = pd.read_csv('docs/{}/{}.csv'.format(item['country'], item['file_name']), sep=',')
            #if the item exists in the file it will be checked for update
            if (df.Title == item['title']).any():
                if (df.loc[df.Title == item['title'], 'Date']).any():
                    if (df[df.Title == item['title']]['Date'] != item['date']).any():
                        df.loc[df.Title == item['title'], 'Date'] = item['date']
                        df.loc[df.Title == item['title'], 'Text_diff_new'] = str(set(item['text']).difference(ast.literal_eval((df[df.Title == item['title']]['Text']).item())))
                        df.loc[df.Title == item['title'], 'Text_diff_old'] = str(set(ast.literal_eval((df[df.Title == item['title']]['Text']).item())).difference(item['text']))
                        df.loc[df.Title == item['title'], 'Text'] = str(item['text'])
                        if (df.loc[df.Title == item['title'], 'Text_diff_new'] != 'set()').any() or (df.loc[df.Title == item['title'], 'Text_diff_old'] != 'set()').any():
                            t_new = df[df.Title == item['title']]['Text_diff_new'][3]
                            t_old = df[df.Title == item['title']]['Text_diff_old'][3]
                            self.tracking(item, t_new, t_old)
                else:
                    if ast.literal_eval((df[df.Title == item['title']]['Text']).item()) != item['text']:
                        df.loc[df.Title == item['title'], 'Text_diff_new'] = str(set(item['text']).difference(ast.literal_eval((df[df.Title == item['title']]['Text']).item())))
                        df.loc[df.Title == item['title'], 'Text_diff_old'] = str(set(ast.literal_eval((df[df.Title == item['title']]['Text']).item())).difference(item['text']))
                        df.loc[df.Title == item['title'], 'Text'] = str(item['text'])
                        t_new = df[df.Title == item['title']]['Text_diff_new'][3]
                        t_old = df[df.Title == item['title']]['Text_diff_old'][3]
                        self.tracking(item, t_new, t_old)
            else:
                if item.get('date'):
                    df = pd.concat([df, pd.DataFrame.from_records([{'Title': item['title'], 'Date': item['date'], 'Text': item['text']}])])
                else:
                    df = pd.concat([df, pd.DataFrame.from_records([{'Title': item['title'], 'Text': item['text']}])])
            df.to_csv('docs/{}/{}.csv'.format(item['country'], item['file_name']), sep=',', index=False)
            
        return item

    def tracking(self, item, t_new, t_old):
        df = pd.read_csv('docs/tracking.csv', sep=',')
        if item.get('date'):
            df = pd.concat([df, pd.DataFrame.from_records([{'Country': item['country'], 'Title': item['title'], 'Date': item['date'], 'Url': item['url'], 'Text_new': t_new, 'Text_old': t_old}])])
        else:
            df = pd.concat([df, pd.DataFrame.from_records([{'Country': item['country'], 'Title': item['title'], 'Url': item['url'], 'Text_new': t_new, 'Text_old': t_old}])])
        df.to_csv('docs/tracking.csv', sep=',', index=False)
        # send_note(item)

    # def close_spider(self, spider, item):
        # send_note(item)

#This pipeline is for files download
class RtffilesPipeline(FilesPipeline):
    stat = 0

    #here you can change file name and storage location
    def file_path(self, request, response=None, info=None, *, item=RtffilesItem):
        if request.url.endswith('.pdf') or request.url.endswith('.rtf'):
            file_name: str = request.url.split("/")[-1][:-4] + '_' + str(datetime.datetime.now())[:10] + request.url.split("/")[-1][-4:]
        else:
            file_name: str = request.url.split("/")[-1].replace('.ashx?', '').replace('=', '') + '_' + str(datetime.datetime.now())[:10] + '.pdf'
        return '%s/%s' % (item['country'], file_name)

    #this method needs for camparison file versions
    def inc_stats(self, spider, status):
        super(RtffilesPipeline, self).inc_stats(spider=spider, status=status)
        if status == 'downloaded':
            RtffilesPipeline.stat = 1

#This pipeline is for comaprison documents
class CompareVersionsPipeline():
    def process_item(self, item, spider):
        if isinstance(item, RtffilesItem) and RtffilesPipeline.stat == 1:
            self.get_files_list(item)
        return item


    def get_files_list(self, item):
        dic_files = {}
        files = [file[:4] for file in os.listdir(f"docs/{item['country']}")]
        for file in os.listdir(f"docs/{item['country']}"):
            for j in set(files):
                if file.startswith(j):
                    if dic_files.get(j):
                        dic_files[j].append(file)
                    else:
                        dic_files[j] = [file]
        # print(files)
        # print(dic_files)

        for i in dic_files:
            if len(dic_files[i]) == 2:
                self.check_rtf(item, dic_files[i])

    #convert pdf->docx or rtf->docx and compare two docx files
    def check_rtf(self, item, files):
        if files[0].endswith('rtf'):
            for i in files:
                ConvertRtfToDocx(item, i)    
        elif files[0].endswith('pdf'):
            for i in files:
                convert_pdf(item, i)
        compare_doc(item, files)