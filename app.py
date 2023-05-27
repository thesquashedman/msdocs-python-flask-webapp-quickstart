from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route('/')
def connection():
    
    cnxn = mysql.connector.connect(user="thesquashedman", password="#cooldude2", host="pavelserver.mysql.database.azure.com", port=3306, database="library")
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM book;")
    

    html = "<table>"
    row = cursor.fetchone() 
    while row:
        html += "<tr>"
        for item in row:
            html += "<td>" + str(item) + "</td>"
        html += "</tr>"
        print (row) 
        row = cursor.fetchone()
    html += "</table>"
    return html
