from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
import mysql.connector

import os

from mysql.connector import errorcode

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
        try:
            cursor.execute(
                "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, A.Author_name, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies " 
                "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE title like '%"+ name +"%') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
                "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE title like '%"+ name +"%') as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C, "
                "Author as A "
                "WHERE C.isbn = L.isbn AND A.author_ID = L.author_ID;")
            tabledata = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err.msg)
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
        try:
            cursor.execute(
                "SELECT L.ISBN, L.Title, L.address, Z.city, Z.state, L.zip_code, L.shelf, L.copies_owned, COUNT(C.book_isbn) as copies_checked_out, L.copies_owned - COUNT(C.book_isbn) as copies_available, MIN(C.return_date) as next_return_date "
                "FROM "
                "(SELECT B.*, address, zip_code, copies_owned, shelf FROM (SELECT * FROM BOOK WHERE title like '%"+ name +"%') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn) as L "
                "LEFT JOIN "
                "BOOKS_CHECKED_OUT as C "
                "ON L.isbn = C.book_isbn AND L.address = C.address AND L.zip_code = C.zip_code, "
                "LIBRARY as Z "
                "WHERE Z.address = L.address AND Z.zip_code = L.zip_code "
                "GROUP BY L.isbn, L.address, L.zip_code;")
            
            tabledata2 = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err.msg)
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
        header2.append("Next Return Date (yy-mm-dd)")
        search = "Searching for books with '" + name + "' in Title" 
        locations = "Locations for books with '" + name + "' in Title" 
    elif request.form['searchbutton'] == 'genre':
        name = request.form.get('name')
        try:
            cursor.execute(
                "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, A.Author_Name, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies "
                "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE genre = '"+ name +"') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
                "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE genre = '"+ name +"') as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C, "
                "Author as A "
                "WHERE C.isbn = L.isbn AND A.author_ID = L.author_ID;")
            tabledata = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err.msg)
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
        
        try:
            cursor.execute(
                "SELECT L.ISBN, L.Title, L.address, Z.city, Z.state, L.zip_code, L.shelf, L.copies_owned, COUNT(C.book_isbn) as copies_checked_out, L.copies_owned - COUNT(C.book_isbn) as copies_available, MIN(C.return_date) as next_return_date "
                "FROM "
                "(SELECT B.*, address, zip_code, copies_owned, shelf FROM (SELECT * FROM BOOK WHERE genre = '"+ name +"') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn) as L "
                "LEFT JOIN "
                "BOOKS_CHECKED_OUT as C "
                "ON L.isbn = C.book_isbn AND L.address = C.address AND L.zip_code = C.zip_code, "
                "LIBRARY as Z "
                "WHERE Z.address = L.address AND Z.zip_code = L.zip_code "
                "GROUP BY L.isbn, L.address, L.zip_code;")
            
            tabledata2 = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err.msg)
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
        header2.append("Next Return Date (yy-mm-dd)")
        search = "Searching for books with genre '" + name + "'" 
        locations = "Locations for books with genre '" + name + "'" 
    elif request.form['searchbutton'] == 'ISBN':
        name = request.form.get('name')
        try:
            cursor.execute(
                "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, A.Author_Name, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies "
                "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE ISBN = '"+ name +"') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
                "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE ISBN = '"+ name +"') as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C, "
                "Author as A "
                "WHERE C.isbn = L.isbn AND A.author_ID = L.author_ID;")
            tabledata = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err.msg)
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
        
        try:
            cursor.execute(
                "SELECT L.ISBN, L.Title, L.address, Z.city, Z.state, L.zip_code, L.shelf, L.copies_owned, COUNT(C.book_isbn) as copies_checked_out, L.copies_owned - COUNT(C.book_isbn) as copies_available, MIN(C.return_date) as next_return_date "
                "FROM "
                "(SELECT B.*, address, zip_code, copies_owned, shelf FROM (SELECT * FROM BOOK WHERE ISBN = '"+ name +"') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn) as L "
                "LEFT JOIN "
                "BOOKS_CHECKED_OUT as C "
                "ON L.isbn = C.book_isbn AND L.address = C.address AND L.zip_code = C.zip_code, "
                "LIBRARY as Z "
                "WHERE Z.address = L.address AND Z.zip_code = L.zip_code "
                "GROUP BY L.isbn, L.address, L.zip_code;")
            
            tabledata2 = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err.msg)
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
        header2.append("Next Return Date (yy-mm-dd)")
        search = "Searching for books with ISBN '" + name + "'" 
        locations = "Locations for books with ISBN '" + name + "'" 
    elif request.form['searchbutton'] == 'Year Published':
        name = request.form.get('name')
        try:
            cursor.execute(
                "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, A.Author_Name, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies "
                "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE Year_published = "+ name +") as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
                "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE Year_published = "+ name +") as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C, "
                "Author as A "
                "WHERE C.isbn = L.isbn AND A.author_ID = L.author_ID;")
            tabledata = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err.msg)
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
        
        try:
            cursor.execute(
                "SELECT L.ISBN, L.Title, L.address, Z.city, Z.state, L.zip_code, L.shelf, L.copies_owned, COUNT(C.book_isbn) as copies_checked_out, L.copies_owned - COUNT(C.book_isbn) as copies_available, MIN(C.return_date) as next_return_date "
                "FROM "
                "(SELECT B.*, address, zip_code, copies_owned, shelf FROM (SELECT * FROM BOOK WHERE Year_Published = "+ name +") as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn) as L "
                "LEFT JOIN "
                "BOOKS_CHECKED_OUT as C "
                "ON L.isbn = C.book_isbn AND L.address = C.address AND L.zip_code = C.zip_code, "
                "LIBRARY as Z "
                "WHERE Z.address = L.address AND Z.zip_code = L.zip_code "
                "GROUP BY L.isbn, L.address, L.zip_code;")
        
            tabledata2 = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err.msg)
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
        header2.append("Next Return Date (yy-mm-dd)")
        search = "Searching for books with Publish Year '" + name + "'" 
        locations = "Locations for books with Publish Year '" + name + "'" 
    elif request.form['searchbutton'] == 'Publisher':
        name = request.form.get('name')
        try:
            cursor.execute(
                "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, A.Author_Name, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies "
                "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE publisher like '%"+ name +"%') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
                "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE publisher like '%"+ name +"%') as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C, "
                "Author as A "
                "WHERE C.isbn = L.isbn AND A.author_ID = L.author_ID;")
            tabledata = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err.msg)
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
        
        try:
            cursor.execute(
                "SELECT L.ISBN, L.Title, L.address, Z.city, Z.state, L.zip_code, L.shelf, L.copies_owned, COUNT(C.book_isbn) as copies_checked_out, L.copies_owned - COUNT(C.book_isbn) as copies_available, MIN(C.return_date) as next_return_date "
                "FROM "
                "(SELECT B.*, address, zip_code, copies_owned, shelf FROM (SELECT * FROM BOOK WHERE Publisher LIKE '%"+ name +"%') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn) as L "
                "LEFT JOIN "
                "BOOKS_CHECKED_OUT as C "
                "ON L.isbn = C.book_isbn AND L.address = C.address AND L.zip_code = C.zip_code, "
                "LIBRARY as Z "
                "WHERE Z.address = L.address AND Z.zip_code = L.zip_code "
                "GROUP BY L.isbn, L.address, L.zip_code;")
            
            tabledata2 = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err.msg)
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
        header2.append("Next Return Date (yy-mm-dd)")
        search = "Searching for books with Publisher with'" + name + "'" 
        locations = "Locations for books with Publisher with'" + name + "'" 
    elif request.form['searchbutton'] == 'Language':
        name = request.form.get('name')
        try:
            cursor.execute(
                "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, A.Author_name, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies "
                "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT * FROM BOOK WHERE language like '%"+ name +"%') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
                "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT * FROM BOOK WHERE language like '%"+ name +"%') as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C, "
                "Author as A "
                "WHERE C.isbn = L.isbn AND A.author_ID = L.author_ID;")
            tabledata = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err.msg)
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

        try:
            cursor.execute(
                "SELECT L.ISBN, L.Title, L.address, Z.city, Z.state, L.zip_code, L.shelf, L.copies_owned, COUNT(C.book_isbn) as copies_checked_out, L.copies_owned - COUNT(C.book_isbn) as copies_available, MIN(C.return_date) as next_return_date "
                "FROM "
                "(SELECT B.*, address, zip_code, copies_owned, shelf FROM (SELECT * FROM BOOK WHERE Language LIKE '%"+ name +"%') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn) as L "
                "LEFT JOIN "
                "BOOKS_CHECKED_OUT as C "
                "ON L.isbn = C.book_isbn AND L.address = C.address AND L.zip_code = C.zip_code, "
                "LIBRARY as Z "
                "WHERE Z.address = L.address AND Z.zip_code = L.zip_code "
                "GROUP BY L.isbn, L.address, L.zip_code;")
            
            tabledata2 = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err.msg)
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
        header2.append("Next Return Date (yy-mm-dd)")
        search = "Searching for books with Language with '" + name + "'" 

        locations = "Locations for books with Language with '" + name + "'" 
    elif request.form['searchbutton'] == 'Author':
        name = request.form.get('name')
        try:
            cursor.execute(
                "SELECT L.ISBN, L.Title, L.Year_published, L.Genre, L.Publisher, L.Language, L.Author_Name, total_copies, copies_checked_out, total_copies - copies_checked_out as available_copies "
                "FROM (SELECT B.*, SUM(copies_owned) as total_copies FROM (SELECT B.*, Author_name FROM BOOK as B, Author as A WHERE Author_name like '%"+ name +"%' AND B.author_ID = A.author_ID) as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn GROUP BY B.isbn) as L, " 
                "(SELECT B.*, COUNT(C.book_isbn) as copies_checked_out FROM (SELECT B.*, Author_name FROM BOOK as B, Author as A WHERE Author_name like '%"+ name +"%' AND B.author_ID = A.author_ID) as B left join BOOKS_CHECKED_OUT as C on B.isbn = C.book_isbn GROUP BY isbn) as C "
                "WHERE C.isbn = L.isbn;")
            tabledata = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err.msg)
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

        try:
            cursor.execute(
                "SELECT L.ISBN, L.Title, L.address, Z.city, Z.state, L.zip_code, L.shelf, L.copies_owned, COUNT(C.book_isbn) as copies_checked_out, L.copies_owned - COUNT(C.book_isbn) as copies_available, MIN(C.return_date) as next_return_date "
                "FROM "
                "(SELECT B.*, address, zip_code, copies_owned, shelf FROM (SELECT B.*, Author_name FROM BOOK as B, Author as A WHERE Author_name like '%"+ name +"%' AND B.author_ID = A.author_ID) as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn) as L "
                "LEFT JOIN "
                "BOOKS_CHECKED_OUT as C "
                "ON L.isbn = C.book_isbn AND L.address = C.address AND L.zip_code = C.zip_code, "
                "LIBRARY as Z "
                "WHERE Z.address = L.address AND Z.zip_code = L.zip_code "
                "GROUP BY L.isbn, L.address, L.zip_code;")
            
            tabledata2 = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err.msg)
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
        header2.append("Next Return Date (yy-mm-dd)")
        search = "Searching for books with Author with '" + name + "'" 
        locations = "Locations for books with Author with '" + name + "'" 

    return render_template('index.html', ptable = tabledata, header = header, ptable2 = tabledata2, header2 = header2, search = search, locations = locations)
    """
    if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
    else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))
    """
@app.route('/checkout')
def checkoutStart():
   print('Request for checkout page received')
   return render_template('checkout.html')
@app.route('/checkout', methods=['POST'])
def checkout():
    global cnxn
    global cursor
    tabledata = []
    header = []
    temp = None
    errorMessage = ""
    try:
        cursor.execute(
            "SELECT MAX(Reference_ID) FROM BOOKS_CHECKED_OUT")
        
        temp = cursor.fetchall()
    except mysql.connector.Error as err:
        print(err.msg) 
        errorMessage = "Real Bad Error"
    if(temp != None):
        print (int(''.join(map(str, temp[0]))))
        checkoutid = int(''.join(map(str, temp[0]))) + 1
        customer = request.form.get('customer')
        address = request.form.get('address')
        zip = request.form.get('zip')
        isbn = request.form.get('ISBN')

        tempTable = None
        #Check that library has book and that it isn't checked out
        try:
            cursor.execute(
                "SELECT L.copies_owned - COUNT(C.book_isbn) as copies_available "
                "FROM "
                "(SELECT B.*, address, zip_code, copies_owned, shelf FROM (SELECT * FROM BOOK WHERE ISBN = '"+ isbn +"') as B left join LIBRARY_OWNS_BOOKS as L on B.isbn = L.isbn WHERE L.address = '" + address + "' AND L.zip_code = " + zip + ") as L "
                "LEFT JOIN "
                "BOOKS_CHECKED_OUT as C "
                "ON L.isbn = C.book_isbn AND L.address = C.address AND L.zip_code = C.zip_code "
                "GROUP BY L.isbn, L.address, L.zip_code;")
            
            tempTable = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err.msg)
            errorMessage = "Bad Inputs"
        if(tempTable != None and len(tempTable) != 1):
            errorMessage = "Book at address not found"
        if(tempTable != None and len(tempTable) == 1):
            if(int(''.join(map(str, tempTable[0]))) <= 0):
                errorMessage = "Checkout Failed, All copies checked out"
            else:
                success = True
                try:
                    print("INSERT INTO BOOKS_CHECKED_OUT (Reference_ID, Customer_library_card, Book_ISBN, Address, Zip_code, Return_date) VALUES (" + str(checkoutid) + ", " + customer + ", '" + isbn + "', '" + address + "', " + zip + ", DATE_ADD(now(), INTERVAL 7 DAY));")
                    cursor.execute(
                        "INSERT INTO BOOKS_CHECKED_OUT (Reference_ID, Customer_library_card, Book_ISBN, Address, Zip_code, Return_date) VALUES (" + str(checkoutid) + ", " + customer + ", '" + isbn + "', '" + address + "', " + zip + ", DATE_ADD(now(), INTERVAL 7 DAY));")
                    cnxn.commit()
                    errorMessage = "checkout successful"
                except mysql.connector.Error as err:
                    print(err.msg)
                    errorMessage = "Customer Not Found"
                    success = False
                if(success == True):
                    try:
                        cursor.execute(
                            "Select Book_ISBN, Address, Zip_code, return_date FROM BOOKS_CHECKED_OUT WHERE Customer_library_card = '" + customer + "';")
                        tabledata = cursor.fetchall()
                    except mysql.connector.Error as err:
                        print(err.msg)
                    header.append("ISBN")
                    header.append("Address")
                    header.append("Zip")
                    header.append("Return Date (yy-mm-dd)")
                    
                
                    

    return render_template('checkout.html', error = errorMessage, ptable = tabledata, header = header)

    


@app.route('/librarian')
def librarianStart():
    print('Request for librarian page received')
    return render_template('librarian.html')

@app.route('/librarianOverdue', methods=['POST'])
def searchOverdue():
    global cursor
    tabledata = []
    header = []
    errorMessage = ""



    Search = request.form.get('searchQuery')
    if len(Search) > 0:
        try:
            cursor.execute(
                "SELECT CUSTOMER.Library_card_number "
                "FROM CUSTOMER "
                "WHERE CUSTOMER.Library_card_number = " + Search)

            tempTable = cursor.fetchall()

            if len(tempTable) == 0:
                errorMessage = "No Customer found"
                return render_template('librarian.html', error1=errorMessage)

        except mysql.connector.Error as err:
            print(err.msg)
            errorMessage = "ERROR: Bad Inputs"

        Search = "AND Library_card_number = " + Search
    else:
        Search = ""

    try:
        cursor.execute(
            ##HAD TO HARD CODE DATE, 'NOW' ISNT WORKING
            "SELECT BOOK.title, CHECKED.Name, CHECKED.Return_date "
            "FROM BOOK, ( "
            "SELECT * "
            "FROM CUSTOMER, BOOKS_CHECKED_OUT AS BCO "
            "WHERE CUSTOMER.Library_card_number = BCO.Customer_library_card) AS CHECKED "
            "WHERE BOOK.ISBN = CHECKED.Book_ISBN "
            "AND CHECKED.Return_date < DATE('2023-06-07') "
            + Search)


        tabledata = cursor.fetchall()
        header.append("Title")
        header.append("Customer name")
        header.append("Original return date")

    except mysql.connector.Error as err:
        print(err.msg)
        errorMessage = "Real Bad Error"
    if len(tabledata) == 0:
        errorMessage = "No overdue books"
        return render_template('librarian.html', error1 = errorMessage)



    return render_template('librarian.html', error1 = errorMessage, header = header, tabledata = tabledata)


@app.route('/librarian', methods=['POST'])
def addBook():
    global cnxn
    global cursor
    tempTable = None
    errorMessage = ""

    ISBN = request.form.get('ISBN')
    Title = request.form.get('Title')
    Year_published = request.form.get('Year_published')
    Genre = request.form.get('Genre')
    Publisher = request.form.get('Publisher')
    Language = request.form.get('Language')
    Author_ID = request.form.get('Author_ID')

    try:
        cursor.execute(
            "SELECT BOOK.ISBN "
            "FROM BOOK "
            "WHERE BOOK.ISBN = " + ISBN)

        tempTable = cursor.fetchall()

        if len(tempTable) > 0:
            errorMessage = "ERROR: Book already exists!"
            return render_template('librarian.html', error2 =errorMessage)

    except mysql.connector.Error as err:
        print(err.msg)
        errorMessage = "ERROR: Bad Inputs"
    try:
        cursor.execute(
            "SELECT AUTHOR.Author_ID "
            "FROM AUTHOR "
            "WHERE  AUTHOR.Author_ID= " + Author_ID)

        tempTable = cursor.fetchall()

        if len(tempTable) == 0:
            errorMessage = "Author does not yet exist!"
            return render_template('librarian.html', error2 =errorMessage)

    except mysql.connector.Error as err:
        print(err.msg)
        errorMessage = "ERROR: Bad Inputs"

    try:
        print(Title)
        cursor.execute(
            "INSERT INTO BOOK (ISBN, Title, Year_published, Genre, Publisher, Language, Author_ID) VALUES ('" + ISBN +"', '" + Title + "', " + Year_published + ", '" + Genre + "', '" + Publisher + "', '" + Language + "', '" + Author_ID + "');"
        )
        cnxn.commit()
        errorMessage = "Success!"

    except mysql.connector.Error as err:
        print(err.msg)
        errorMessage = "ERROR: Bad Inputs"



    return render_template('librarian.html', error2 =errorMessage)



if __name__ == '__main__':
   app.run()

