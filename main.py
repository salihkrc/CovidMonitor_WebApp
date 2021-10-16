from flask import Flask, render_template
import Downloader, scrapePDF
import datetime
import  db_connection
pdfpath = "./PDF/covid-gr-daily-report-"+str(datetime.datetime.today().strftime('%Y%m%d'))+".pdf"

app = Flask(__name__)

@app.route("/")
def index():

    date = datetime.datetime.today().strftime('%Y-%m-%d')
    cases = scrapePDF.extractPDF(pdfpath,"cases") #TODO get from EODY PDF
    num_test = int(scrapePDF.extractTests(pdfpath,"PCR")) + int(scrapePDF.extractPDF(pdfpath,"rapid")) #TODO get from EODY PDF
    positivity = cases/num_test
    # shots = 0 # TODO vax info from EODY
    #coverage = 0 # TODO vax info from EODY

    return render_template("index.html", cases=cases, date=date, num_test=num_test, positivity=positivity)

if __name__ == "__main__":
    app.run()


