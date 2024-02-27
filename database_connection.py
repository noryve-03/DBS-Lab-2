"""
Contains a context manager for a database connection.

Author: Rami Pellumbi - SP24
"""
import psycopg2


DB_NAME = 'library'       # newly created local database
USER = 'freeman'        # replace with your username (might be postgres)
PASSWORD = ''             # replace with your password (might be empty)
HOST = 'localhost'        # host postgres is running on
PORT = '5432'             # default port that postgres listens on


class DatabaseConnection:
    """
    This class is a context manager for a database connection.
    It automatically establishes a connection to the database when the context
    is entered and closes the connection when the context is exited.

    Example Usage:
    ```
    with DatabaseConnection() as cursor:
        cursor.execute('SELECT * FROM library;')
        results = cursor.fetchall()
        print(results)
    ```
    """
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        config = {
            'dbname': DB_NAME,
            'user': USER,
            'password': PASSWORD,
            'host': HOST,
            'port': PORT
        }
        self.connection = psycopg2.connect(**config)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

        if exc_type or exc_val or exc_tb:
            print(f'Error: {exc_type}, {exc_val}, {exc_tb}')
