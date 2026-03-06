
# Imported sqlite3
import sqlite3

# Created a connection to the database.db file
connection = sqlite3.connect('database.db')

# Read the schema.sql file and execute the SQL script to create the tables
with open('schema.sql', 'r') as f:
    sql_script = f.read()

# Executed SQL script to create tables in database
connection.executescript(sql_script)

# Save the connection
connection.commit()

print("Database setup complete.")

# Created a cursor to execute SQL commands
cursor = connection.cursor()

# Check if status is inserted correctly by selecting all from Status table
cursor.execute("SELECT * FROM Status")

# Fetch all results and print them
result = cursor.fetchall()
for row in result:
    print(f"Status_ID: {row[0]}, Status_Name: {row[1]}")

# Close the connection
connection.close()