import urllib.request

import scrapePDF
import db_connection
import datetime

date = datetime.datetime(2021, 5, 1) #start counting from 2021/05/01

while date.strftime('%Y%m%d') <= datetime.datetime.today().strftime('%Y%m%d'):
    print(date.strftime(('%Y%m%d')))
    print(date.strftime('%Y'))
    print(date.strftime('%m'))
    ret = urllib.request.urlretrieve("https://eody.gov.gr/wp-content/uploads/"+str(date.strftime('%Y'))+"/"+str(date.strftime('%m'))+"/covid-gr-daily-report-"+str(date.strftime('%Y%m%d'))+".pdf", "./dbFillerScript/covid-gr-daily-report-"+str(date.strftime('%Y%m%d'))+".pdf")


    pdfpath = "./dbFillerScript/covid-gr-daily-report-"+str(date.strftime('%Y%m%d'))+".pdf"
    PCR = scrapePDF.extractTests(pdfpath,"PCR")
    Rapid = scrapePDF.extractPDF(pdfpath, "rapid")
    cases = scrapePDF.extractPDF(pdfpath,'cases')
    deaths = scrapePDF.extractPDF(pdfpath,'deaths')



    date += datetime.timedelta(days=1)



