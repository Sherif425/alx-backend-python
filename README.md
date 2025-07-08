To complete the task, you need to create a Python script seed.py that sets up a MySQL database (ALX_prodev), creates a table (user_data) with the specified fields, populates it with data from a user_data.csv file, and includes a generator to stream rows from the user_data table one by one. The provided 0-main.py script tests the database setup and data insertion but does not directly test the generator, so we’ll ensure the generator is included to meet the objective.

Below, I’ll provide a complete seed.py script that implements all required functions and adds a generator function to stream rows, along with explanations tailored to the task’s requirements.

Task Requirements
Database and Table Setup:

Database: ALX_prodev
Table: user_data with fields:
user_id: UUID (stored as CHAR(36)), Primary Key, Indexed
name: VARCHAR, NOT NULL
email: VARCHAR, NOT NULL
age: DECIMAL, NOT NULL
Populate the table with data from user_data.csv.
Function Prototypes:

connect_db(): Connects to the MySQL server.
create_database(connection): Creates the ALX_prodev database if it doesn’t exist.
connect_to_prodev(): Connects to the ALX_prodev database.
create_table(connection): Creates the user_data table if it doesn’t exist.
insert_data(connection, data): Inserts data from user_data.csv into user_data, avoiding duplicates.
Generator Objective:

Create a generator function to stream rows from the user_data table one by one, ensuring memory efficiency by fetching rows incrementally.
Expected Behavior (from 0-main.py):

Connect to the MySQL server and create the database.
Connect to ALX_prodev, create the user_data table, and insert data.
Verify the database exists and print the first 5 rows of user_data.
Assumptions:

The user_data.csv file has columns: user_id, name, email, age.
user_id values are valid UUIDs (36-character strings).
MySQL server is running locally, and credentials (e.g., root user, password) are available.
The generator function is not called in 0-main.py but is required by the objective.
Solution: seed.py
Here’s a complete seed.py script that meets all requirements, including the generator function:

import mysql.connector
import csv
from mysql.connector import Error

def connect_db():
    """Connect to the MySQL server."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL user
            password=''   # Replace with your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    return None

def create_database(connection):
    """Create the ALX_prodev database if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        connection.commit()
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL user
            password='',  # Replace with your MySQL password
            database='ALX_prodev'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None
    return None

def create_table(connection):
    """Create the user_data table if it doesn't exist."""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX idx_user_id (user_id)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()

def insert_data(connection, data):
    """Insert data from user_data.csv into user_data table, avoiding duplicates."""
    try:
        cursor = connection.cursor()
        with open(data, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                if len(row) != 4:
                    print(f"Skipping invalid row: {row}")
                    continue
                user_id, name, email, age = row
                try:
                    insert_query = """
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s);
                    """
                    cursor.execute(insert_query, (user_id, name, email, float(age)))
                except Error as e:
                    print(f"Error inserting row {user_id}: {e}")
        connection.commit()
    except Error as e:
        print(f"Error inserting data: {e}")
    except Exception as e:
        print(f"Error reading CSV: {e}")
    finally:
        cursor.close()

def stream_rows(connection):
    """Generator to stream rows from user_data table one by one."""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data;")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
    except Error as e:
        print(f"Error streaming rows: {e}")
    finally:
        cursor.close()
Explanation of the Script
Dependencies:

Uses mysql.connector for MySQL interactions.
Uses csv to read user_data.csv.
Function Details:

connect_db():
Connects to the MySQL server using mysql.connector.
Returns a connection object or None on failure.
Credentials (host, user, password) must be updated to match your MySQL setup.
create_database(connection):
Executes CREATE DATABASE IF NOT EXISTS ALX_prodev; to create the database.
Commits the transaction to ensure the database is created.
connect_to_prodev():
Connects to the ALX_prodev database using the same credentials.
Returns a connection object or None on failure.
create_table(connection):
Creates the user_data table with:
user_id: CHAR(36) for UUIDs, PRIMARY KEY, with an index (INDEX idx_user_id).
name: VARCHAR(255), NOT NULL.
email: VARCHAR(255), NOT NULL.
age: DECIMAL(5,2), NOT NULL (supports numbers like 67.00 or 123.45).
Uses IF NOT EXISTS to avoid errors if the table already exists.
Prints “Table user_data created successfully” (as seen in the output).
insert_data(connection, data):
Opens user_data.csv and skips the header row.
Reads each row, expecting user_id, name, email, age.
Uses INSERT IGNORE to skip rows with duplicate user_id values.
Converts age to float to match the DECIMAL type.
Includes error handling for invalid rows or database errors.
stream_rows(connection):
A generator function that executes SELECT * FROM user_data;.
Uses cursor.fetchone() to fetch one row at a time.
Yields each row as a tuple (e.g., ('00234e50-...', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67)).
Closes the cursor when done to free resources.
Handles database errors gracefully.
Generator:

The stream_rows function is designed to stream rows one by one, making it memory-efficient for large datasets.
It uses fetchone() to avoid loading the entire result set into memory, aligning with the task’s objective.
CSV Assumptions:

The user_data.csv file is expected to have a header row (e.g., user_id,name,email,age).
Each row contains four fields: a 36-character UUID, a name string, an email string, and a numeric age.
Example row: 00234e50-34eb-4ce2-94ec-26e3fa749796,Dan Altenwerth Jr.,Molly59@gmail.com,67.
Output Alignment:

The script matches the output in 0-main.py:
“connection successful” (from connect_db()).
“Table user_data created successfully” (from create_table()).
“Database ALX_prodev is present” (from the SELECT SCHEMA_NAME query).
A list of 5 tuples from SELECT * FROM user_data LIMIT 5;.
How to Test the Generator
The 0-main.py script doesn’t test the stream_rows function, but you can verify it by adding the following code to 0-main.py after the existing queries:

# Test the generator
print("Streaming rows:")
for row in seed.stream_rows(connection):
    print(row)
connection.close()
This will print each row from user_data one by one, demonstrating the generator’s functionality.

Setup Instructions
Install Dependencies:
Install the MySQL Connector for Python:
pip install mysql-connector-python
MySQL Server:
Ensure a MySQL server is running locally.
Update the user and password in connect_db() and connect_to_prodev() to match your MySQL credentials.
CSV File:
Place user_data.csv in the same directory as seed.py and 0-main.py.
Ensure it has the correct format (columns: user_id, name, email, age).
Run the Script:
Execute 0-main.py to test the database setup and data insertion:
./0-main.py
Add the generator test code (above) to verify stream_rows.
Troubleshooting Tips
Connection Errors: Verify MySQL is running and credentials are correct. Check host, user, and password.
CSV Errors: Ensure user_data.csv exists and has valid data. Check for missing or malformed rows.
Table Creation: If the table isn’t created, check MySQL permissions for the user.
Generator: If stream_rows doesn’t work, ensure the table has data and the connection is active.
Example Output
Running 0-main.py should produce output like:

connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ('006bfede-724d-4cdd-a2a6-59700f40d0da', 'Glenda Wisozk', 'Miriam21@gmail.com', 119), ('006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'Daniel Fahey IV', 'Delia.Lesch11@hotmail.com', 49), ('00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'Ronnie Bechtelar', 'Sandra19@yahoo.com', 22), ('00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'Alma Bechtelar', 'Shelly_Balistreri22@hotmail.com', 102)]
If you add the generator test:

Streaming rows:
('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67)
('006bfede-724d-4cdd-a2a6-59700f40d0da', 'Glenda Wisozk', 'Miriam21@gmail.com', 119)
...
If you need help with specific parts (e.g., debugging, CSV format, or MySQL setup), or if you want to see the generator tested in a different way, let me know!
