# from PyPDF2 import PdfFileReader
import os

os.chdir('c:/job/python/TAR_EMEAR/doc_test')


# with open('c:/job/python/TAR_EMEAR/doc_test/graniza_pp_14012019.pdf', 'rb') as file:
    
    # pdf = PdfFileReader(file)
# print(pdf.getNumPages())
    # first_page = pdf.getPage(0)

    # print(first_page.extractText())
# print(pdf.documentInfo)

# for page in pdf.pages:
    # print(page.extractText())
from pdf2docx import Converter
# import os

# # # dir_path for input reading and output files & a for loop # # #

path_input = 'c:/job/python/TAR_EMEAR/doc_test/1/'
path_output = 'c:/job/python/TAR_EMEAR/doc_test/'
file = '1960.03.15_2022-04-01.pdf'
# for file in os.listdir(path_input):

cv = Converter(path_input+file)
cv.convert(path_output+file+'.docx', start=0, end=None)
cv.close()
    # print(file)
