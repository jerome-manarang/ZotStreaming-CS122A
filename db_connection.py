###this just creates the connection to mysql
#change this depending on ur connection
###change this for gradescope : mysql.connector.connect(user='test', password='password', database='cs122a')


import mysql.connector

def connect_db():
    return mysql.connector.connect(
        #host="localhost",
        user="test",
        password="password",
        database="cs122a"
    )
