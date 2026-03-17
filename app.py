import sqlite3 # Import sqlite3 module 
import flask # Import Flask 
from flask import Flask, render_template, request, redirect, url_for # import Flask and render_template from flask

app = Flask(__name__) # Creating a Flask application

def get_db_connection():
    conn = sqlite3.connect('database.db') # Conecting sqlite3 database
    conn.row_factory = sqlite3.Row # set row factory to sqlite3.row to access columns by name
    return conn # Returns database connection

@app.route('/') # Define a route for root url, so whenever user visits the root url, index function will be called
def index(): # Defining a function to handle root url
    conn = get_db_connection() # Getting database connection
    try:
        books = conn.execute("SELECT Item.*, Author.Author_Name, Status.Status_Name FROM Item JOIN Author ON Item.Author_ID = Author.Author_ID JOIN Status ON Item.Status_ID = Status.Status_ID").fetchall() # Execute SQL query selecting all records from Item table
        return render_template('index.html', books=books) # Render the index.html template and pass books variable to it
    finally:
        conn.close() # Closing the database connection

@app.route('/manage') # Define a route for manage url
def manage():
    conn = get_db_connection() # Getting database connection
    try:
        books = conn.execute("SELECT Item.*, Author.Author_Name, Status.Status_Name FROM Item JOIN Author On Item.Author_ID = Author.Author_ID JOIN Status ON Item.Status_ID = Status.Status_ID").fetchall() # Execute SQL query selecting all records from Item table
        return render_template('manage.html', books=books)  # Render the manage.html template and pass books variable to it
    finally:
        conn.close() # Closing the database connection

@app.route('/stats') # Define a route for stats url
def stats():
    conn = get_db_connection() # Getting database connection
    try:
        total_books = conn.execute("SELECT COUNT(*) From Item").fetchall()[0]
        books_to_read = conn.execute("SELECT Count(Item.Status_ID) FROM Item where Status_ID = 3").fetchall()[0]
        books_reading = conn.execute("SELECT Count(Item.Status_ID) FROM Item where Status_ID = 1").fetchall()[0]
        return render_template('stats.html', total_books=total_books, books_to_read=books_to_read, books_reading=books_reading)
    finally:
        conn.close() # Closing the database connection

@app.route('/add_book', methods=['POST']) # Define a route for add url with POST method
def add_book():
    title = request.form['title'] # Get the title from the form
    author_name = request.form['author_name'] # Get the author name from the form
    total_pages = request.form['total_pages'] # Get the total pages from the form
    date = request.form['date_started'] # Get the date started from the form
    description = request.form['description'] # Get the book description from the form

    status_id = 3  # Default to 'To Read' status
    
    conn = get_db_connection() # Getting database connection
    try:
        author = conn.execute("SELECT Author_ID FROM Author WHERE Author_Name = ?", (author_name,)).fetchone() # Finds if Author ID already exists

        if author: # If Author ID exists, use existing Author ID
            author_id = author['Author_ID']
        else: # If Author ID does not exist, insert a new Author and get the new Author ID from the last row
            cur = conn.execute("INSERT INTO Author (Author_Name) VALUES (?)", (author_name,))
            conn.commit()
            author_id = cur.lastrowid # Get the last inserted Author_ID

        conn.execute("INSERT INTO Item (Title, Author_ID, Status_ID, Total_Pages, Date_Started, Book_Description) VALUES (?, ?, ?, ?, ?, ?)", (title, author_id, status_id, total_pages, date, description)) # Execute SQL query to insert a new record into Item table
        conn.commit() # Commit the changes to the database
        return redirect(url_for('manage')) # Redirect to the manage page after adding a book
    finally:
        conn.close() # Closing the database connection

@app.route('/get_book/<int:book_id>', methods=['GET']) # Define a route for get_book url with GET method and book_id as a perimeter
def get_book(book_id): # Define a function to get a book by its ID
    conn = get_db_connection() # Getting database connection
    try:
        book = conn.execute("SELECT Item.*, Author.Author_Name, Status.Status_Name FROM Item JOIN Author on Item.Author_ID = Author.Author_ID JOIN Status on Item.Status_ID = Status.Status_ID Where Item.Item_ID = ?", (book_id,)).fetchone() #Execute SQL query to select all books with its ID and joins the Author and Status tables to get the author name and status name

        if book: # If book exists, return book details as JSON response
            return flask.jsonify({'book': dict(book)})
        else: # If book does not exist, return error message
            return flask.jsonify({'error': 'Book not found'}), 404
    finally:
        conn.close() # Closing the database connection

@app.route('/delete_book/<int:book_id>', methods=['POST']) # Define a route for delete_book url with POST method and book_id as a perimeter
def delete_book(book_id): # Define a function to delete a book by its ID
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM Item WHERE Item_ID = ?", (book_id,))
        conn.commit()
        return flask.jsonify({'success': True})
    finally:
        conn.close() # Closing the database connection

@app.route('/edit_book/<int:book_id>', methods=['POST'])
def edit_book(book_id): # Defining a function to edit the book by its ID
    conn = get_db_connection() # Geting database connection
    try: # Requesting the form data from the edit book form and storing it into variables
        title = request.form['title']
        author_name = request.form['author']
        status_id = request.form['status']
        pages_read = request.form['pages_read']
        total_pages = request.form['total_pages']
        rating = request.form['rating']
        date_started = request.form['date_started']
        date_finished = request.form['date_finished']
        description = request.form['description']
        author = conn.execute("SELECT Author_ID FROM Author WHERE Author_Name = ?", (author_name,)).fetchone() # Finds if Author ID already exists

        if author:
            author_id = author['Author_ID'] # If Author ID exists, use existing Author ID
        else:
            cur = conn.execute("INSERT INTO Author (Author_Name) VALUES (?)", (author_name,))
            conn.commit() # Committing the changes to the database after inserting a new Author
            author_id = cur.lastrowid # Adding author if it does not exist and getting the new Author ID from the last row

        conn.execute("UPDATE Item SET Title = ?, Author_ID = ?, Status_ID = ?, Pages_Read = ?, Total_Pages = ?, Rating = ?,Date_Started = ?, Date_Finished = ?, Book_Description = ? WHERE Item_ID = ?", (title, author_id, status_id, pages_read, total_pages, rating, date_started, date_finished, description, book_id)) # Updating the book with the values from the form
        conn.commit() # Committing the changes to the database after updating the book
        return redirect(url_for('manage')) # Returning to the manage page after editing the book
    finally:
        conn.close() # Closing the database connection
    

    

if __name__ == '__main__':
    app.run(debug=True) # Run the Flask application in debug mode