import mysql.connector

def connect_db():
    connect = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="fletapp"
    )
    return connect