# seed.py
import mysql.connector
import csv
import os
from dotenv import load_dotenv
import uuid # Import the uuid module

# Load environment variables from .env file
load_dotenv()

def connect_db():
    """
    Connects to the MySQL database server.
    Returns a connection object if successful, None otherwise.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "password")
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created or already exists.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.
    Returns a connection object if successful, None otherwise.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "password"),
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev database: {err}")
        return None

def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields.
    Note: UUIDs are stored as VARCHAR(36) in MySQL.
    """
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5, 0) NOT NULL
        )
        """
        cursor.execute(create_table_query)
        print("Table user_data created successfully.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def insert_data(connection, csv_file_path):
    """
    Inserts data from a CSV file into the user_data table.
    Generates a UUID for user_id if not present in the CSV.
    Data is inserted only if a user with the same user_id does not already exist.
    """
    try:
        cursor = connection.cursor()
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Generate UUID if user_id is not in the CSV or is empty
                user_id = row.get('user_id')
                if not user_id:
                    user_id = str(uuid.uuid4()) # Generate a new UUID
                    print(f"Generated UUID for a row: {user_id}")
                
                name = row['name']
                email = row['email']
                age = int(row['age'])

                # Check if the user_id already exists before inserting
                check_query = "SELECT user_id FROM user_data WHERE user_id = %s"
                cursor.execute(check_query, (user_id,))
                result = cursor.fetchone()

                if result is None:
                    insert_query = """
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (user_id, name, email, age))
                    print(f"Inserted data for user_id: {user_id}")
                else:
                    print(f"User with user_id {user_id} already exists. Skipping insertion.")
            connection.commit()
        cursor.close()
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

