import re
import datetime

import pdfplumber

#pdfpath = "./PDF/covid-gr-daily-report-"+str(datetime.datetime.today().strftime('%Y%m%d'))+".pdf"

def extractTests(pdfpath,testFlag): # For PCR Flag=PCR, For Rapid Flag=Rapid
    pdf = pdfplumber.open(pdfpath)
    page = pdf.pages[4]
    text = page.extract_text()
    #print(text)

    if testFlag=="PCR":

        res = text.split('έχουνσυνολικάελεγχθεί', maxsplit=1)[-1]\
                .split(maxsplit=1)[0]
    else:
        res = text.split('RapidAgέχουνελεγχθεί', maxsplit=1)[-1]\
            .split(maxsplit=1)[0]

    #print("\n",str(res))
    number = re.findall(r'[0-9]+', res)
    s = [str(i) for i in number]
    fin_num = int("".join(s))
    #number = int(float(a_string))
    pdf.close()
    #print(fin_num)
    return fin_num


def extractPDF(pdfpath,Flag): # Flag=death, Flag=cases
    pdf = pdfplumber.open(pdfpath)
    if Flag=="cases":
        page = pdf.pages[0]
    else:
        page = pdf.pages[1]
    text = page.extract_text()


    if Flag=="cases":

        res = text.split('καταγράφηκαντιςτελευταίες24ώρεςείναι', maxsplit=1)[-1]\
                .split(maxsplit=1)[0]
    else:
        buf = text.split('ΟινέοιθάνατοιασθενώνμεCOVID-19είναι', maxsplit=1)[-1] \
            .split(maxsplit=1)[0]
        buffer = buf.split(",")
        res=buffer[0]
        return res



    number = re.findall(r'[0-9]+', res)
    s = [str(i) for i in number]
    fin_num = int("".join(s))
    #number = int(float(a_string))
    pdf.close()

    return fin_num

def dias(pdfpath):
    #def extractTests(pdfpath, testFlag):  # For PCR Flag=PCR, For Rapid Flag=Rapid
        pdf = pdfplumber.open(pdfpath)
        page = pdf.pages[2]
        text = page.extract_text()



        buf = text.split('εύονταιδιασωληνωμένοιείναι', maxsplit=1)[-1] \
        .split(maxsplit=1)[0]


        buffer = buf.split("(")
        res = buffer[0]
        return res




