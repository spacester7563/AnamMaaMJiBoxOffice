import mysql.connector
from flask import current_app

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='root',
        database='Movie_Booking'
    )
    return conn
