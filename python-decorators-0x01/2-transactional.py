import sqlite3
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open database connection
        conn = sqlite3.connect('users.db')
        try:
            # Call the original function with the connection and other arguments
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Ensure the connection is closed
            conn.close()
    return wrapper

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Begin transaction
            conn.execute("BEGIN TRANSACTION")
            # Call the original function
            result = func(conn, *args, **kwargs)
            # Commit transaction if no errors
            conn.commit()
            return result
        except Exception as e:
            # Rollback transaction on error
            conn.rollback()
            raise e
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
