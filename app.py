from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
import mysql.connector
app = Flask(__name__)

global cnxn
global cursor
cnxn = mysql.connector.connect(user="thesquashedman", password="#cooldude2", host="pavelserver.mysql.database.azure.com", port=3306, database="library")
   
cursor = cnxn.cursor()


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
    global cnxn
    global cursor
    tabledata = []
    header = []
    tabledata2 = []
    header2 = []
    search = ""
    locations = ""
    if request.form['searchbutton'] == 'title':
        name = request.form.get('name')
        cursor.execute(
            "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, A.Author_name, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies " 
            "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE title like '%"+ name +"%') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
            "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE title like '%"+ name +"%') as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C, "
            "Author as A "
            "WHERE C.isbn = L.isbn AND A.author_ID = L.author_ID;")
        tabledata = cursor.fetchall()
        header.append("ISBN")
        header.append("Title")
        header.append("Year Published")
        header.append("Genre")
        header.append("Publisher")
        header.append("Language")
        header.append("Author")
        header.append("Total Copies")
        header.append("Copies Checked Out")
        header.append("Copies Available")
        
        #cnxn2 = mysql.connector.connect(user="thesquashedman", password="#cooldude2", host="pavelserver.mysql.database.azure.com", port=3306, database="library")
        #cursor2 = cnxn.cursor()
        cursor.execute(
            "SELECT L.ISBN, L.Title, L.address, Z.city, Z.state, L.zip_code, L.shelf, L.copies_owned, COUNT(C.book_isbn) as copies_checked_out, L.copies_owned - COUNT(C.book_isbn) as copies_available "
            "FROM "
            "(SELECT B.*, address, zip_code, copies_owned, shelf FROM (SELECT * FROM BOOK WHERE title like '%"+ name +"%') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn) as L "
            "LEFT JOIN "
            "BOOKS_CHECKED_OUT as C "
            "ON L.isbn = C.book_isbn AND L.address = C.address AND L.zip_code = C.zip_code, "
            "LIBRARY as Z "
            "WHERE Z.address = L.address AND Z.zip_code = L.zip_code "
            "GROUP BY L.isbn, L.address, L.zip_code;")
        
        tabledata2 = cursor.fetchall()
        header2.append("ISBN")
        header2.append("Title")
        header2.append("Address")
        header2.append("City")
        header2.append("State")
        header2.append("Zip Code")
        header2.append("Shelf")
        header2.append("Copies Owned")
        header2.append("Copies Checked Out")
        header2.append("Copies Available")
        search = "Searching for books with '" + name + "' in Title" 
        locations = "Locations for books with '" + name + "' in Title" 
    elif request.form['searchbutton'] == 'genre':
        name = request.form.get('name')
        cursor.execute(
            "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, A.Author_Name, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies "
            "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE genre = '"+ name +"') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
            "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE genre = '"+ name +"') as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C, "
            "Author as A "
            "WHERE C.isbn = L.isbn AND A.author_ID = L.author_ID;")
        tabledata = cursor.fetchall()
        header.append("ISBN")
        header.append("Title")
        header.append("Year Published")
        header.append("Genre")
        header.append("Publisher")
        header.append("Language")
        header.append("Author")
        header.append("Total Copies")
        header.append("Copies Checked Out")
        header.append("Copies Available")
        
        cursor.execute(
            "SELECT L.ISBN, L.Title, L.address, Z.city, Z.state, L.zip_code, L.shelf, L.copies_owned, COUNT(C.book_isbn) as copies_checked_out, L.copies_owned - COUNT(C.book_isbn) as copies_available "
            "FROM "
            "(SELECT B.*, address, zip_code, copies_owned, shelf FROM (SELECT * FROM BOOK WHERE genre = '"+ name +"') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn) as L "
            "LEFT JOIN "
            "BOOKS_CHECKED_OUT as C "
            "ON L.isbn = C.book_isbn AND L.address = C.address AND L.zip_code = C.zip_code, "
            "LIBRARY as Z "
            "WHERE Z.address = L.address AND Z.zip_code = L.zip_code "
            "GROUP BY L.isbn, L.address, L.zip_code;")
        
        tabledata2 = cursor.fetchall()
        header2.append("ISBN")
        header2.append("Title")
        header2.append("Address")
        header2.append("City")
        header2.append("State")
        header2.append("Zip Code")
        header2.append("Shelf")
        header2.append("Copies Owned")
        header2.append("Copies Checked Out")
        header2.append("Copies Available")
        search = "Searching for books with genre '" + name + "'" 
        locations = "Locations for books with genre '" + name + "'" 
    elif request.form['searchbutton'] == 'ISBN':
        name = request.form.get('name')
        cursor.execute(
            "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, A.Author_Name, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies "
            "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE ISBN = '"+ name +"') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
            "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE ISBN = '"+ name +"') as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C, "
            "Author as A "
            "WHERE C.isbn = L.isbn AND A.author_ID = L.author_ID;")
        tabledata = cursor.fetchall()
        header.append("ISBN")
        header.append("Title")
        header.append("Year Published")
        header.append("Genre")
        header.append("Publisher")
        header.append("Language")
        header.append("Author")
        header.append("Total Copies")
        header.append("Copies Checked Out")
        header.append("Copies Available")
        
        cursor.execute(
            "SELECT L.ISBN, L.Title, L.address, Z.city, Z.state, L.zip_code, L.shelf, L.copies_owned, COUNT(C.book_isbn) as copies_checked_out, L.copies_owned - COUNT(C.book_isbn) as copies_available "
            "FROM "
            "(SELECT B.*, address, zip_code, copies_owned, shelf FROM (SELECT * FROM BOOK WHERE ISBN = '"+ name +"') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn) as L "
            "LEFT JOIN "
            "BOOKS_CHECKED_OUT as C "
            "ON L.isbn = C.book_isbn AND L.address = C.address AND L.zip_code = C.zip_code, "
            "LIBRARY as Z "
            "WHERE Z.address = L.address AND Z.zip_code = L.zip_code "
            "GROUP BY L.isbn, L.address, L.zip_code;")
        
        tabledata2 = cursor.fetchall()
        header2.append("ISBN")
        header2.append("Title")
        header2.append("Address")
        header2.append("City")
        header2.append("State")
        header2.append("Zip Code")
        header2.append("Shelf")
        header2.append("Copies Owned")
        header2.append("Copies Checked Out")
        header2.append("Copies Available")
        search = "Searching for books with ISBN '" + name + "'" 
        locations = "Locations for books with ISBN '" + name + "'" 
    elif request.form['searchbutton'] == 'Year Published':
        name = request.form.get('name')
        cursor.execute(
            "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, A.Author_Name, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies "
            "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE Year_published = "+ name +") as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
            "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE Year_published = "+ name +") as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C, "
            "Author as A "
            "WHERE C.isbn = L.isbn AND A.author_ID = L.author_ID;")
        tabledata = cursor.fetchall()
        header.append("ISBN")
        header.append("Title")
        header.append("Year Published")
        header.append("Genre")
        header.append("Publisher")
        header.append("Language")
        header.append("Author")
        header.append("Total Copies")
        header.append("Copies Checked Out")
        header.append("Copies Available")
        
        cursor.execute(
            "SELECT L.ISBN, L.Title, L.address, Z.city, Z.state, L.zip_code, L.shelf, L.copies_owned, COUNT(C.book_isbn) as copies_checked_out, L.copies_owned - COUNT(C.book_isbn) as copies_available "
            "FROM "
            "(SELECT B.*, address, zip_code, copies_owned, shelf FROM (SELECT * FROM BOOK WHERE Year_Published = "+ name +") as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn) as L "
            "LEFT JOIN "
            "BOOKS_CHECKED_OUT as C "
            "ON L.isbn = C.book_isbn AND L.address = C.address AND L.zip_code = C.zip_code, "
            "LIBRARY as Z "
            "WHERE Z.address = L.address AND Z.zip_code = L.zip_code "
            "GROUP BY L.isbn, L.address, L.zip_code;")
        
        tabledata2 = cursor.fetchall()
        header2.append("ISBN")
        header2.append("Title")
        header2.append("Address")
        header2.append("City")
        header2.append("State")
        header2.append("Zip Code")
        header2.append("Shelf")
        header2.append("Copies Owned")
        header2.append("Copies Checked Out")
        header2.append("Copies Available")
        search = "Searching for books with Publish Year '" + name + "'" 
        locations = "Locations for books with Publish Year '" + name + "'" 
    elif request.form['searchbutton'] == 'Publisher':
        name = request.form.get('name')
        cursor.execute(
            "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, A.Author_Name, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies "
            "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE publisher like '%"+ name +"%') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
            "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE publisher like '%"+ name +"%') as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C, "
            "Author as A "
            "WHERE C.isbn = L.isbn AND A.author_ID = L.author_ID;")
        tabledata = cursor.fetchall()
        header.append("ISBN")
        header.append("Title")
        header.append("Year Published")
        header.append("Genre")
        header.append("Publisher")
        header.append("Language")
        header.append("Author")
        header.append("Total Copies")
        header.append("Copies Checked Out")
        header.append("Copies Available")
        
        cursor.execute(
            "SELECT L.ISBN, L.Title, L.address, Z.city, Z.state, L.zip_code, L.shelf, L.copies_owned, COUNT(C.book_isbn) as copies_checked_out, L.copies_owned - COUNT(C.book_isbn) as copies_available "
            "FROM "
            "(SELECT B.*, address, zip_code, copies_owned, shelf FROM (SELECT * FROM BOOK WHERE Publisher LIKE '%"+ name +"%') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn) as L "
            "LEFT JOIN "
            "BOOKS_CHECKED_OUT as C "
            "ON L.isbn = C.book_isbn AND L.address = C.address AND L.zip_code = C.zip_code, "
            "LIBRARY as Z "
            "WHERE Z.address = L.address AND Z.zip_code = L.zip_code "
            "GROUP BY L.isbn, L.address, L.zip_code;")
        
        tabledata2 = cursor.fetchall()
        header2.append("ISBN")
        header2.append("Title")
        header2.append("Address")
        header2.append("City")
        header2.append("State")
        header2.append("Zip Code")
        header2.append("Shelf")
        header2.append("Copies Owned")
        header2.append("Copies Checked Out")
        header2.append("Copies Available")
        search = "Searching for books with Publisher with'" + name + "'" 
        locations = "Locations for books with Publisher with'" + name + "'" 
    elif request.form['searchbutton'] == 'Language':
        name = request.form.get('name')
        cursor.execute(
            "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, A.Author_ID, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies "
            "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE language like '%"+ name +"%') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
            "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE language like '%"+ name +"%') as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C, "
            "Author as A "
            "WHERE C.isbn = L.isbn AND A.author_ID = L.author_ID;")
        tabledata = cursor.fetchall()
        header.append("ISBN")
        header.append("Title")
        header.append("Year Published")
        header.append("Genre")
        header.append("Publisher")
        header.append("Language")
        header.append("Author")
        header.append("Total Copies")
        header.append("Copies Checked Out")
        header.append("Copies Available")

        cursor.execute(
            "SELECT L.ISBN, L.Title, L.address, Z.city, Z.state, L.zip_code, L.shelf, L.copies_owned, COUNT(C.book_isbn) as copies_checked_out, L.copies_owned - COUNT(C.book_isbn) as copies_available "
            "FROM "
            "(SELECT B.*, address, zip_code, copies_owned, shelf FROM (SELECT * FROM BOOK WHERE Language LIKE '%"+ name +"%') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn) as L "
            "LEFT JOIN "
            "BOOKS_CHECKED_OUT as C "
            "ON L.isbn = C.book_isbn AND L.address = C.address AND L.zip_code = C.zip_code, "
            "LIBRARY as Z "
            "WHERE Z.address = L.address AND Z.zip_code = L.zip_code "
            "GROUP BY L.isbn, L.address, L.zip_code;")
        
        tabledata2 = cursor.fetchall()
        header2.append("ISBN")
        header2.append("Title")
        header2.append("Address")
        header2.append("City")
        header2.append("State")
        header2.append("Zip Code")
        header2.append("Shelf")
        header2.append("Copies Owned")
        header2.append("Copies Checked Out")
        header2.append("Copies Available")
        search = "Searching for books with Language with '" + name + "'" 
        locations = "Locations for books with Language with '" + name + "'" 
        
    return render_template('index.html', ptable = tabledata, header = header, ptable2 = tabledata2, header2 = header2, search = search, locations = locations)
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