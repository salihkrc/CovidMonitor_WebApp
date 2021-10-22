from io import StringIO
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import re

def scrape(pdfpath):
    # PDFMiner Analyzers
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = "utf-8"
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # path to our input file
    pdf_file = pdfpath

    # Extract text
    pdfFile = open(pdf_file, "rb")
    for page in PDFPage.get_pages(pdfFile):
        interpreter.process_page(page)
    #fp.close()

    # Return text from StringIO
    text = sio.getvalue()



    # Freeing Up
    device.close()
    sio.close()
    return text

#pdfpath = "./PDF/covid-gr-daily-report-"+str(datetime.datetime.today().strftime('%Y%m%d'))+".pdf"

def extractTests(text,testFlag): # For PCR Flag=PCR, For Rapid Flag=Rapid


    if testFlag=="PCR":

        res = text.split("το σύνολο των δειγμάτων που ελέγχουν, έχουν συνολικά ελεγχθεί ")[1].split()[0]
    else:
        res = text.split('διενεργούν ελέγχους Rapid Ag έχουν ελεγχθεί ')[1].split()[0]



    return re.sub('[.]', '', res)


def extractPDF(text,Flag): # Flag=death, Flag=cases


    if Flag=="cases":

        res = text.split('καταγράφηκαν τις τελευταίες 24 ώρες είναι')[1].split()[0]


    else:
        try:
            buf = text.split('Οι νέοι θάνατοι ασθενών με COVID-19 είναι')[1].split()[0]

            return re.sub('[.,]', '', buf)
        except Exception as e:
            buf = text.split('Οι νέοι θάνατοι ασθενών με COVID-19 που καταγράφηκαν τις τελευταίες 48 ώρες είναι')[1].split()[0]
            print(e)
            return re.sub('[.,]', '', buf)


    return re.sub('[.,]', '', res)

def dias(text):




        buf = text.split('νοσηλεύονται διασωληνωμένοι είναι')[1].split()[0]


        #print("res: ", res)

        return buf




