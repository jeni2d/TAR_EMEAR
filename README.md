# TAR_EMEAR

This is scrapy project for getting info about transport access restrictions from governmental sites in European countries.

Each spider is for one web site.

There are two main pipelines, one is for sites with attached documents, and another is for sites where the information is stored on the web page itself.

There is a repository for each parsed site.

For attached documents -> all records are stored in SQLite DB -> if the release date will be changed, a new document will be downloaded and compared with the previous one.
All formats will be converted to Docx then two Docx files will be compared.

For sites with the information on themself -> parsed information is stored in CSV files -> if the release date will be changed, all items will be compared with each other.

All differences are stored in the tracking file.

If any difference will be reached the delta will be sent to the responsible person using Gmail API.

!!!Project is not finished yet:
Email module is not finished,
Module for deleting old files and cleaning tracking should be created,
Parsers are ready only for 22 countries. 


