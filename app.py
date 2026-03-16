import sqlite3 # Import sqlite3 module 
import flask # Import Flask 
from flask import Flask, render_template, request, redirect, url_for # import Flask and render_template from flask

app = Flask(__name__) # Creating a Flask application

def get_db_connection():
    conn = sqlite3.connect('database.db') # Conecting sqlite3 database
    conn.row_factory = sqlite3.Row # set row factory to sqlite3.row to access columns by name
    return conn

@app.route('/') # Define a route for root url
def index():
    conn = get_db_connection() # Getting database connection
    books = conn.execute("SELECT Item.*, Author.Author_Name, Status.Status_Name FROM Item JOIN Author ON Item.Author_ID = Author.Author_ID JOIN Status ON Item.Status_ID = Status.Status_ID").fetchall() # Execute SQL query selecting all records from Item table
    conn.close() # Closing the database connection
    return render_template('index.html', books=books) # Render the index.html template and pass books variable to it

@app.route('/manage') # Define a route for manage url
def manage():
    conn = get_db_connection() # Getting database connection
    books = conn.execute("SELECT Item.*, Author.Author_Name, Status.Status_Name FROM Item JOIN Author On Item.Author_ID = Author.Author_ID JOIN Status ON Item.Status_ID = Status.Status_ID").fetchall() # Execute SQL query selecting all records from Item table
    conn.close() # Closing the database connection
    return render_template('manage.html', books=books)  # Render the manage.html template and pass books variable to it

@app.route('/stats') # Define a route for stats url
def stats():
    conn = get_db_connection() # Getting database connection
    total_books = conn.execute("SELECT COUNT(*) From ITEM").fetchall()[0]
    books_to_read = conn.execute("SELECT Count(Item.Status_ID) FROM ITEM where Status_ID = 3").fetchall()[0]
    books_reading = conn.execute("SELECT Count(Item.Status_ID) FROM ITEM where Status_ID = 1").fetchall()[0]
    conn.close() # Closing the database connection
    return render_template('stats.html', total_books=total_books, books_to_read=books_to_read, books_reading=books_reading)

@app.route('/add_book', methods=['POST']) # Define a route for add url with POST method
def add_book():
    title = request.form['title'] # Get the title from the form
    author_name = request.form['author_name'] # Get the author name from the form
    total_pages = request.form['total_pages'] # Get the total pages from the form
    status_id = 3  # Default to 'To Read' status
    
    conn = get_db_connection() # Getting database connection
    author = conn.execute("SELECT Author_ID FROM Author WHERE Author_Name = ?", (author_name,)).fetchone()

    if author:
        author_id = author['Author_ID']
    else:
        cur = conn.execute("INSERT INTO Author (Author_Name) VALUES (?)", (author_name,))
        conn.commit()
        author_id = cur.lastrowid

    conn.execute("INSERT INTO Item (Title, Author_ID, Status_ID, Total_Pages) VALUES (?, ?, ?, ?)", (title, author_id, status_id, total_pages)) # Execute SQL query to insert a new record into Item table
    conn.commit() # Commit the changes to the database
    conn.close() # Closing the database connection
    return redirect(url_for('manage')) # Redirect to the manage page after adding a book


if __name__ == '__main__':
    app.run(debug=True) # Run the Flask application in debug mode