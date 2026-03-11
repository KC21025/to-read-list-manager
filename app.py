import sqlite3 # Import sqlite3 module 
import flask # Import Flask 
from flask import Flask, render_template # import Flask and render_template from flask

app = Flask(__name__) # Creating a Flask application

def get_db_connection():
    conn = sqlite3.connect('database.db') # Conecting sqlite3 database
    conn.row_factory = sqlite3.Row # set row factory to sqlite3.row to access columns by name
    return conn

@app.route('/') # Define a route for root url
def index():
    conn = get_db_connection() # Getting database connection
    books = conn.execute("SELECT * FROM Item").fetchall() # Execute SQL query selecting all records from Item table
    conn.close() # Closing the database connection
    return render_template('index.html', books=books) # Render the index.html template and pass books variable to it

if __name__ == '__main__':
    app.run(debug=True) # Run the Flask application in debug mode