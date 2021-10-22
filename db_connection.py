import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(host='localhost',
                                     database='covidmonitor_db',
                                     user='cvdmonitor-user',
                                     password='')
db_info = connection.get_server_info()
