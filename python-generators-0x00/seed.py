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
