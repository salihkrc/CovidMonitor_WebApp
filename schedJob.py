import urllib.request
from urllib.error import HTTPError

import scrapePDF
import db_connection
import datetime
import os
import glob
import plotChart
import emailDispatcher


def schedjob():
    print("Start Scheduled Process...")

    date = datetime.datetime.today() #start counting from 2021/05/01
    cursor = db_connection.connection.cursor()
    log_text = str((date.strftime(('%Y%m%d'))))
    log_text += str(date.strftime('%Y'))
    log_text += str((date.strftime('%m')))
    try:
        log_text += str( "sending request to: https://eody.gov.gr/wp-content/uploads/" + str(
            date.strftime('%Y')) + "/" + str(date.strftime('%m')) + "/covid-gr-daily-report-" + str(
            date.strftime('%Y%m%d')) + ".pdf")
        try:
            ret = urllib.request.urlretrieve("https://eody.gov.gr/wp-content/uploads/"+str(date.strftime('%Y'))+"/"+str(date.strftime('%m'))+"/covid-gr-daily-report-"+str(date.strftime('%Y%m%d'))+".pdf", "./PDF/covid-gr-daily-report-"+str(date.strftime('%Y%m%d'))+".pdf")
            log_text+=("Firstly, sending request to: https://eody.gov.gr/wp-content/uploads/"+str(date.strftime('%Y'))+"/"+str(date.strftime('%m'))+"/covid-gr-daily-report-"+str(date.strftime('%Y%m%d'))+".pdf")
        except HTTPError as err:
            if err.code == 404:
                try:
                    log_text += str(err), "First Attempt To Download Failed... procceeding to the new one "
                    log_text += ("sending request to: https://eody.gov.gr/wp-content/uploads/" + str(
                        date.strftime('%Y')) + "/" + str(
                        date.strftime('%m')) + "/covid-gr-daily-report-" + str(date.strftime('%Y%m%d')) + "2.pdf")
                    ret = urllib.request.urlretrieve(
                        "https://eody.gov.gr/wp-content/uploads/" + str(date.strftime('%Y')) + "/" + str(
                            date.strftime('%m')) + "/covid-gr-daily-report-" + str(date.strftime('%Y%m%d')) + "2.pdf",
                        "./PDF/covid-gr-daily-report-" + str(date.strftime('%Y%m%d')) + ".pdf")
                except HTTPError as err1:

                    if err1.code ==404:
                        log_text += str(err1), "First Attempt To Download Failed... procceeding to the new one "
                        try:
                            log_text+="sending request to: https://eody.gov.gr/wp-content/uploads/" + str(
                                    date.strftime('%Y')) + "/" + str(
                                    date.strftime('%m')) + "/covid-gr-daily-report-" + str(
                                    date.strftime('%Y%m%d')) + "-2.pdf"
                            ret = urllib.request.urlretrieve(
                                    "https://eody.gov.gr/wp-content/uploads/" + str(date.strftime('%Y')) + "/" + str(
                                        date.strftime('%m')) + "/covid-gr-daily-report-" + str(
                                        date.strftime('%Y%m%d')) + "-2.pdf",
                                    "./PDF/covid-gr-daily-report-" + str(date.strftime('%Y%m%d')) + ".pdf")
                        except Exception as e:
                                log_text += str(e), "No such a file on EODY System"




        text = scrapePDF.scrape(pdfpath="./PDF/covid-gr-daily-report-"+str(date.strftime('%Y%m%d'))+".pdf")
        log_text+=("covid-gr-daily-report-"+str(date.strftime('%Y%m%d'))+".pdf")
    #print(text)


    #pdfpath = "covid-gr-daily-report-"+str(date.strftime('%Y%m%d'))+".pdf"
        PCR = scrapePDF.extractTests(text,"PCR")
        Rapid = scrapePDF.extractTests(text, "rapid")
        cases = scrapePDF.extractPDF(text,'cases')
        deaths = scrapePDF.extractPDF(text,'deaths')
        dias = scrapePDF.dias(text)
        #yesterday = date - datetime.timedelta(days=1)
        log_text+= str(("deaths:",str(deaths), "dias: ", str(dias)))


        datafromSQL = cursor.execute("SELECT * FROM records WHERE R_id = (SELECT max(R_id) FROM records)")
        result_tuple = cursor.fetchall()
        result = list(result_tuple[0])
        #print(result_tuple)
        #print(result)

        #print("Entering to the phase of tests calculation:", "PCR today:",int(PCR),"--",PCR,"-",int(result[1]),"--",result[1],"+", int(Rapid), "--",Rapid,"-",int(result[2]),"--",result[2])

        tests_today = (int(PCR) - int(result[1]) + (int(Rapid) - int(result[2])))

        log_text+=str(("cases:", str(cases), '\n',"tests today:", tests_today))

        Positivity = int(cases) / int(tests_today)

        pushDataToDB = cursor.execute("INSERT INTO records VALUES (%s,%s,%s,%s,%s,%s,%s)",(date.strftime('%Y%m%d'),PCR, Rapid, Positivity, cases,deaths,dias,))

        log_text+=str(("data added to DB date:",date))
        db_connection.connection.commit()

        plotChart.plotChart()
        files = glob.glob('./PDF/*')
        for f in files:
            os.remove(f)



        emailDispatcher.sendEmail(log_text,"Succeed")


    except Exception as exception:
        mail_content=str(log_text+'\n'+str(exception))
        emailDispatcher.sendEmail(mail_content,"Failed")
        print(exception)



