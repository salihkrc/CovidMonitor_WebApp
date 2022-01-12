from flask import Flask, render_template
import datetime
import  db_connection

#pdfpath = "./PDF/covid-gr-daily-report-"+str(datetime.datetime.today().strftime('%Y%m%d'))+".pdf"

app = Flask(__name__)






@app.route("/")
def index():
    cursor = db_connection.connection.cursor()

    latestR_id = cursor.execute("SELECT * FROM records WHERE R_id = (SELECT max(R_id) FROM records )")
    result_tuple = cursor.fetchall()
    result = list(result_tuple[0])


    R_id = result[0]


    dataFromSql = cursor.execute("SELECT * FROM records WHERE R_id = %s",(R_id,) )
    result_tuple = cursor.fetchall()
    result = list(result_tuple[0])

    dataOfYesterdayFromSql = cursor.execute("SELECT * FROM records WHERE R_id = (SELECT max(R_id) FROM records where R_id != %s);",(R_id,))
    result_tuple_yesterday = cursor.fetchall()
    result_yesterday = list(result_tuple_yesterday[0])


    date = datetime.datetime.today().strftime('%Y-%m-%d')
    cases = result[4]
    num_test = (int(result[1]) - int(result_yesterday[1])) + (int(result[2]) - result_yesterday[2])
    positivity = round(float(result[3]), 4)

    dias = result[6]
    deaths = result[5]




    return render_template("index.html", cases=cases, date=date, num_test=num_test, positivity=positivity, dias=dias,deaths=deaths)

if __name__ == "__main__":
    app.run(debug=True)


