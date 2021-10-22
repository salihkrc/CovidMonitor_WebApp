import db_connection
import matplotlib.pyplot as plt

def plotChart():
    cursor = db_connection.connection.cursor()
    dataFromSql = cursor.execute("SELECT * FROM records order by R_id desc limit 10" )
    result_tuple = cursor.fetchall()
    result_ = list(result_tuple)
    listOflist=[]
    for rec in result_:
        listOflist.append(list(rec))


    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [listOflist[0][3],listOflist[1][3],listOflist[2][3],listOflist[3][3],listOflist[4][3],listOflist[5][3],listOflist[6][3],listOflist[7][3],listOflist[8][3],listOflist[9][3]]
    plt.plot(x,y)

    plt.xlabel('Days')
    plt.ylabel('Positivity')
    plt.title('Positivity in last 10 days ')
    plt.legend(['Positivity'])

# save the figure
    plt.savefig('static/plot.png', dpi=300, bbox_inches='tight')




