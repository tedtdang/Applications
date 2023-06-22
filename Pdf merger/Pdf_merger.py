from pathlib import Path as p
from PyPDF2 import PdfMerger, PdfFileReader
import inspect

folder_path = 'D:\BitBucket/5222\Project\Readings'
file = '20131226051740869.pdf'

# merger = PdfMerger()
# for item in glob(f'{path_source}/*.pdf'):
#     merger.append(item)
#
# merger.write(f'{path_source}/Merged.pdf')
# merger.close()

# def extracting_data(path):
#     with open(path, 'rb') as file:
#         reader = PdfFileReader(file)
#         info = reader.getDocumentInfo()
#         page_number = reader.getNumPages()
#     text = f"""
#     {info = }
#     {page_number = }
#     """
#     return text
#
# print(extracting_data(p.join(path_source, 'Merged.pdf')))
