import urllib.request
from urllib.error import HTTPError

import scrapePDF
import db_connection
import datetime

date = datetime.datetime(2021, 12, 21
                         ) #start counting from 2021/05/01
cursor = db_connection.connection.cursor()

while date.strftime('%Y%m%d') <= datetime.datetime.today().strftime('%Y%m%d'):
    print(date.strftime(('%Y%m%d')))
    print(date.strftime('%Y'))
    print(date.strftime('%m'))
    try:
        print("Firstly, sending request to: https://eody.gov.gr/wp-content/uploads/" + str(
            date.strftime('%Y')) + "/" + str(date.strftime('%m')) + "/covid-gr-daily-report-" + str(
            date.strftime('%Y%m%d')) + ".pdf")
        try:
            ret = urllib.request.urlretrieve("https://eody.gov.gr/wp-content/uploads/"+str(date.strftime('%Y'))+"/"+str(date.strftime('%m'))+"/covid-gr-daily-report-"+str(date.strftime('%Y%m%d'))+".pdf", "covid-gr-daily-report-"+str(date.strftime('%Y%m%d'))+".pdf")
            print("Firstly, sending request to: https://eody.gov.gr/wp-content/uploads/"+str(date.strftime('%Y'))+"/"+str(date.strftime('%m'))+"/covid-gr-daily-report-"+str(date.strftime('%Y%m%d'))+".pdf")
        except HTTPError as err:
            if err.code == 404:
                try:
                    print(err, "First Attempt To Download Failed... procceeding to the new one ")
                    print("sending request to: https://eody.gov.gr/wp-content/uploads/" + str(
                        date.strftime('%Y')) + "/" + str(
                        date.strftime('%m')) + "/covid-gr-daily-report-" + str(date.strftime('%Y%m%d')) + "2.pdf")
                    ret = urllib.request.urlretrieve(
                        "https://eody.gov.gr/wp-content/uploads/" + str(date.strftime('%Y')) + "/" + str(
                            date.strftime('%m')) + "/covid-gr-daily-report-" + str(date.strftime('%Y%m%d')) + "2.pdf",
                        "covid-gr-daily-report-" + str(date.strftime('%Y%m%d')) + ".pdf")
                except HTTPError as err1:

                    if err1.code ==404:
                        print(err1, "First Attempt To Download Failed... procceeding to the new one ")
                        try:
                            print("sending request to: https://eody.gov.gr/wp-content/uploads/" + str(
                                date.strftime('%Y')) + "/" + str(
                                date.strftime('%m')) + "/covid-gr-daily-report-" + str(
                                date.strftime('%Y%m%d')) + "-2.pdf")
                            ret = urllib.request.urlretrieve(
                                "https://eody.gov.gr/wp-content/uploads/" + str(date.strftime('%Y')) + "/" + str(
                                    date.strftime('%m')) + "/covid-gr-daily-report-" + str(
                                    date.strftime('%Y%m%d')) + "-2.pdf",
                                "covid-gr-daily-report-" + str(date.strftime('%Y%m%d')) + ".pdf")
                        except Exception as e:
                            print(e, "No such a file on EODY System")




        text = scrapePDF.scrape(pdfpath="covid-gr-daily-report-"+str(date.strftime('%Y%m%d'))+".pdf")
        print("covid-gr-daily-report-"+str(date.strftime('%Y%m%d'))+".pdf")
    #print(text)


    #pdfpath = "covid-gr-daily-report-"+str(date.strftime('%Y%m%d'))+".pdf"
        PCR = scrapePDF.extractTests(text,"PCR")
        Rapid = scrapePDF.extractTests(text, "rapid")
        cases = scrapePDF.extractPDF(text,'cases')
        deaths = scrapePDF.extractPDF(text,'deaths')
        dias = scrapePDF.dias(text)
        #yesterday = date - datetime.timedelta(days=1)
        print("deaths:",deaths, "dias: ", dias)


        datafromSQL = cursor.execute("SELECT * FROM records WHERE R_id = (SELECT max(R_id) FROM records)")
        result_tuple = cursor.fetchall()
        result = list(result_tuple[0])
        print(result_tuple)
        print(result)

        print("Entering to the phase of tests calculation:", "PCR today:",int(PCR),"--",PCR,"-",int(result[1]),"--",result[1],"+", int(Rapid), "--",Rapid,"-",int(result[2]),"--",result[2])

        tests_today = (int(PCR) - int(result[1]) + (int(Rapid) - int(result[2])))

        print("cases:", cases, '\n',"tests today:", tests_today)

        Positivity = int(cases) / int(tests_today)

        pushDataToDB = cursor.execute("INSERT INTO records VALUES (%s,%s,%s,%s,%s,%s,%s)",(date.strftime('%Y%m%d'),PCR, Rapid, Positivity, cases,deaths,dias,))

        print("data added to DB date:",date)
        db_connection.connection.commit()

        text = '0'

        date += datetime.timedelta(days=1)
    except Exception as exception:
        date += datetime.timedelta(days=1)



