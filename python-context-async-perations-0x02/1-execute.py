# 1-execute.py

import sqlite3

class ExecuteQuery:
    def __init__(self, db_file, query, params=None):
        self.db_file = db_file
        self.query = query
        self.params = params or []
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.commit()
            self.connection.close()

# Usage Example
if __name__ == "__main__":
    db_path = "users.db"  # Ensure this matches the actual path
    query = "SELECT * FROM users WHERE age > ?"
    params = [25]

    with ExecuteQuery(db_path, query, params) as results:
        for row in results:
            print(row)
