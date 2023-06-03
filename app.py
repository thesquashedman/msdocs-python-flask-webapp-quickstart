from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
import mysql.connector
app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['POST'])
def hello():
    cursor = None
    header = []
    if request.form['searchbutton'] == 'title':
        name = request.form.get('name')
        cnxn = mysql.connector.connect(user="thesquashedman", password="#cooldude2", host="pavelserver.mysql.database.azure.com", port=3306, database="library")
        cursor = cnxn.cursor()
        cursor.execute(
            "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, L.Author_ID, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies " 
            "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE title like '%"+ name +"%') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
            "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE title like '%"+ name +"%') as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C "
            "WHERE C.isbn = L.isbn;")
        header.append("ISBN")
        header.append("Title")
        header.append("Year Published")
        header.append("Genre")
        header.append("Publisher")
        header.append("Language")
        header.append("Author ID")
        header.append("Total Copies")
        header.append("Copies Checked Out")
        header.append("Copies Available")
    elif request.form['searchbutton'] == 'genre':
        name = request.form.get('name')
        cnxn = mysql.connector.connect(user="thesquashedman", password="#cooldude2", host="pavelserver.mysql.database.azure.com", port=3306, database="library")
        cursor = cnxn.cursor()
        cursor.execute(
            "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, L.Author_ID, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies "
            "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE genre = '"+ name +"') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
            "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE genre = '"+ name +"') as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C "
            "WHERE C.isbn = L.isbn;")
        header.append("ISBN")
        header.append("Title")
        header.append("Year Published")
        header.append("Genre")
        header.append("Publisher")
        header.append("Language")
        header.append("Author ID")
        header.append("Total Copies")
        header.append("Copies Checked Out")
        header.append("Copies Available")
    elif request.form['searchbutton'] == 'ISBN':
        name = request.form.get('name')
        cnxn = mysql.connector.connect(user="thesquashedman", password="#cooldude2", host="pavelserver.mysql.database.azure.com", port=3306, database="library")
        cursor = cnxn.cursor()
        cursor.execute(
            "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, L.Author_ID, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies "
            "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE ISBN = '"+ name +"') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
            "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE ISBN = '"+ name +"') as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C "
            "WHERE C.isbn = L.isbn;")
        header.append("ISBN")
        header.append("Title")
        header.append("Year Published")
        header.append("Genre")
        header.append("Publisher")
        header.append("Language")
        header.append("Author ID")
        header.append("Total Copies")
        header.append("Copies Checked Out")
        header.append("Copies Available")
    elif request.form['searchbutton'] == 'Year Published':
        name = request.form.get('name')
        cnxn = mysql.connector.connect(user="thesquashedman", password="#cooldude2", host="pavelserver.mysql.database.azure.com", port=3306, database="library")
        cursor = cnxn.cursor()
        cursor.execute(
            "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, L.Author_ID, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies "
            "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE Year_published = "+ name +") as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
            "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE Year_published = "+ name +") as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C "
            "WHERE C.isbn = L.isbn;")
        header.append("ISBN")
        header.append("Title")
        header.append("Year Published")
        header.append("Genre")
        header.append("Publisher")
        header.append("Language")
        header.append("Author ID")
        header.append("Total Copies")
        header.append("Copies Checked Out")
        header.append("Copies Available")
    elif request.form['searchbutton'] == 'Publisher':
        name = request.form.get('name')
        cnxn = mysql.connector.connect(user="thesquashedman", password="#cooldude2", host="pavelserver.mysql.database.azure.com", port=3306, database="library")
        cursor = cnxn.cursor()
        cursor.execute(
            "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, L.Author_ID, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies "
            "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE publisher like '%"+ name +"%') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
            "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE publisher like '%"+ name +"%') as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C "
            "WHERE C.isbn = L.isbn;")
        header.append("ISBN")
        header.append("Title")
        header.append("Year Published")
        header.append("Genre")
        header.append("Publisher")
        header.append("Language")
        header.append("Author ID")
        header.append("Total Copies")
        header.append("Copies Checked Out")
        header.append("Copies Available")
    elif request.form['searchbutton'] == 'Language':
        name = request.form.get('name')
        cnxn = mysql.connector.connect(user="thesquashedman", password="#cooldude2", host="pavelserver.mysql.database.azure.com", port=3306, database="library")
        cursor = cnxn.cursor()
        cursor.execute(
            "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, L.Author_ID, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies "
            "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE language like '%"+ name +"%') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
            "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE language like '%"+ name +"%') as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C "
            "WHERE C.isbn = L.isbn;")
        header.append("ISBN")
        header.append("Title")
        header.append("Year Published")
        header.append("Genre")
        header.append("Publisher")
        header.append("Language")
        header.append("Author ID")
        header.append("Total Copies")
        header.append("Copies Checked Out")
        header.append("Copies Available")
    
    return render_template('index.html', ptable = cursor, header = header)
    """
    if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
    else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))
    """


if __name__ == '__main__':
   app.run()




"""
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
"""