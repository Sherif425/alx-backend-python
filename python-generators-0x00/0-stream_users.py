import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator to stream rows from user_data table one by one as dictionaries."""
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL user
            password='',  # Replace with your MySQL password
            database='ALX_prodev'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT user_id, name, email, age FROM user_data;")
            # Single loop to fetch and yield rows
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                # Yield row as a dictionary
                yield {
                    'user_id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'age': row[3]
                }
    except Error as e:
        print(f"Error streaming rows: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
