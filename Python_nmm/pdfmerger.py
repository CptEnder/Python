"""
Created on Fri 18 Jun 09:32 2021
Finished on
@author: Παύλος Λοΐζου (nm16801)
                                  """
from PyPDF2 import PdfFileMerger, PdfFileReader
import os

mergedObject = PdfFileMerger(strict=False)

for file in os.listdir():
    if file.endswith('.pdf') and file[0] in [str(i) for i in range(11)]:
        mergedObject.append(PdfFileReader(file))

outputFile = "Ερωτημα7.pdf"

mergedObject.write(outputFile)
