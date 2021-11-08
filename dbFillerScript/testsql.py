import fp as fp
import tabula

import db_connection

#cursor = db_connection.connection.cursor()

#results= cursor.execute("SELECT * FROM records")

#myresult = cursor.fetchall()

from io import StringIO
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import scrapePDF


# PDFMiner Analyzers
rsrcmgr = PDFResourceManager()
sio = StringIO()
codec = "utf-8"
laparams = LAParams()
device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)

# path to our input file
pdf_file = "covid-gr-daily-report-20210430.pdf"

# Extract text
pdfFile = open(pdf_file, "rb")
for page in PDFPage.get_pages(pdfFile):
    interpreter.process_page(page)
#fp.close()

# Return text from StringIO
text = sio.getvalue()

print(text)


print("cases:",scrapePDF.extractPDF(text,"cases"))
print("deaths:",scrapePDF.extractPDF(text,"deaths"))

print("PCR:",scrapePDF.extractTests(text,"PCR"))
print("rapid:",scrapePDF.extractTests(text,"rapid"))

print("dias:",scrapePDF.dias(text))




# Freeing Up
device.close()
sio.close()

