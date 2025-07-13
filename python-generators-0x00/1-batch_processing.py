import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """Generator to fetch rows from user_data table in batches."""
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
            # Loop 1: Fetch batches
            while True:
                rows = cursor.fetchmany(batch_size)
                if not rows:
                    break
                # Yield the batch as a list of dictionaries
                yield [
                    {'user_id': row[0], 'name': row[1], 'email': row[2], 'age': row[3]}
                    for row in rows
                ]
    except Error as e:
        print(f"Error fetching batches: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def batch_processing(batch_size):
    """Generator to process batches and yield users over 25."""
    # Loop 2: Iterate over batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 3: Process each user in the batch
        for user in batch:
            if user['age'] > 25:
                yield user
