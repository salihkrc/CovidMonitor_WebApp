import urllib.request
import datetime
import os
import glob

today = datetime.datetime.today()

def DownloadPDF(): # simple download task TODO scheduling
    files = glob.glob('./PDF/*')
    for f in files:
        os.remove(f)


    ret = urllib.request.urlretrieve("https://eody.gov.gr/wp-content/uploads/"+str(today.year)+"/"+str(today.month)+"/covid-gr-daily-report-"+str(datetime.datetime.today().strftime('%Y%m%d'))+".pdf", "./PDF/covid-gr-daily-report-"+str(datetime.datetime.today().strftime('%Y%m%d'))+".pdf")
    return ret
