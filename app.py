from flask import Flask, render_template, request, jsonify
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


@app.route('/api/v1/cases/all', methods=['GET'])
def api_casesAll():
    cursor = db_connection.connection.cursor()
    query = cursor.execute("SELECT R_id,cases FROM records;")
    result_tuple = cursor.fetchall()
    result_list = list(result_tuple)
    result_dic = []
    for rec in result_list:
        line = {"Date": rec[0], "Cases": rec[1]}
        result_dic.append(line)
    # print(result)

    return jsonify(result_dic)

@app.route('/api/v1/cases/range', methods=['GET'])
def api_casesRange():
    range1 = request.args['range1']
    range2 = request.args['range2']

    cursor = db_connection.connection.cursor()
    query = cursor.execute("SELECT R_id,cases FROM records WHERE R_id BETWEEN %s AND %s;", (range1,range2))
    result_tuple = cursor.fetchall()
    result_list = list(result_tuple)
    result_dic = []
    for rec in result_list:
        line = {"Date":rec[0],"Cases":rec[1]}
        result_dic.append(line)
    # print(result)

    return jsonify(result_dic)

@app.route('/api/v1/cases/today', methods=['GET'])
def api_casesToday():
    cursor = db_connection.connection.cursor()
    query = cursor.execute("SELECT R_id,cases FROM records;")
    result_tuple = cursor.fetchall()
    result_list = list(result_tuple)
    result_dic = []

    line = {"Date": result_tuple[len(result_tuple)-1][0], "Cases": result_tuple[len(result_tuple)-1][1]}
    result_dic.append(line)
    # print(result)

    return jsonify(result_dic)








if __name__ == "__main__":
    app.run(debug=True)


