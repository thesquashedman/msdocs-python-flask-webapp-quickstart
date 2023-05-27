from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route('/')
def connection():
    
    cnxn = mysql.connector.connect(user="thesquashedman", password="Mesoepic2", host="pavelserver.mysql.database.azure.com", port=3306, database="library")
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM test;")
    
    row = cursor.fetchone() 
    while row:
        print (row) 
        row = cursor.fetchone()
    return "Connection to database successful"
