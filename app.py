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
    status_id = 3  # Default to 'To Read' status
    
    conn = get_db_connection() # Getting database connection
    try:
        author = conn.execute("SELECT Author_ID FROM Author WHERE Author_Name = ?", (author_name,)).fetchone()

        if author:
            author_id = author['Author_ID']
        else:
            cur = conn.execute("INSERT INTO Author (Author_Name) VALUES (?)", (author_name,))
            conn.commit()
            author_id = cur.lastrowid

        conn.execute("INSERT INTO Item (Title, Author_ID, Status_ID, Total_Pages) VALUES (?, ?, ?, ?)", (title, author_id, status_id, total_pages)) # Execute SQL query to insert a new record into Item table
        conn.commit() # Commit the changes to the database
        return redirect(url_for('manage')) # Redirect to the manage page after adding a book
    finally:
        conn.close() # Closing the database connection

@app.route('/get_book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = get_db_connection()
    try:
        book = conn.execute("SELECT Item.*, Author.Author_Name, Status.Status_Name FROM Item JOIN Author on Item.Author_ID = Author.Author_ID JOIN Status on Item.Status_ID = Status.Status_ID Where Item.Item_ID = ?", (book_id,)).fetchone()

        if book:
            return flask.jsonify({'book': dict(book)})
        else:
            return flask.jsonify({'error': 'Book not found'}), 404
    finally:
        conn.close()

@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM Item WHERE Item_ID = ?", (book_id,))
        conn.commit()
        return flask.jsonify({'success': True})
    finally:
        conn.close()

@app.route('/edit_book/<int:book_id>', methods=['POST'])
def edit_book(book_id):
    conn = get_db_connection()
    try:
        title = request.form['title']
        author_name = request.form['author']
        status_id = request.form['status']
        pages_read = request.form['pages_read']
        total_pages = request.form['total_pages']
        rating = request.form['rating']
        date_started = request.form['date_started']
        date_finished = request.form['date_finished']
        description = request.form['description']
        author = conn.execute("SELECT Author_ID FROM Author WHERE Author_Name = ?", (author_name,)).fetchone()

        if author:
            author_id = author['Author_ID']
        else:
            cur = conn.execute("INSERT INTO Author (Author_Name) VALUES (?)", (author_name,))
            conn.commit()
            author_id = cur.lastrowid

        conn.execute("UPDATE Item SET Title = ?, Author_ID = ?, Status_ID = ?, Pages_Read = ?, Total_Pages = ?, Rating = ?,Date_Started = ?, Date_Finished = ?, Book_Description = ? WHERE Item_ID = ?", (title, author_id, status_id, pages_read, total_pages, rating, date_started, date_finished, description, book_id))
        conn.commit()
        return redirect(url_for('manage'))
    finally:
        conn.close()
    

    

if __name__ == '__main__':
    app.run(debug=True) # Run the Flask application in debug mode