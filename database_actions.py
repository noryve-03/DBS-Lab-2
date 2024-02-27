"""
Utility functions for executing SQL scripts from files and for executing
INSERT commands with psycopg2.
"""
from database_connection import DatabaseConnection


class DatabaseActions:
    """
    This class contains methods for executing SQL scripts from files.

    It injects a DatabaseConnection object to execute the SQL scripts.
    """
    def __init__(self, connection: DatabaseConnection) -> None:
        self.connection = connection

    def execute_file(self, filename: str) -> None:
        """
        This function executes an SQL script from a file.

        It has been provided for you.
        """
        # assert that the filename is a string that ends in .sql
        assert isinstance(filename, str), 'Filename must be a string'
        assert filename.endswith('.sql'), 'Filename must end with .sql'

        # Open the file and read the SQL script
        with open(filename, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        # Execute the SQL script
        with self.connection as cursor:
            cursor.execute(sql_script)

    def execute_insert(self, table_name, fields, values):
        """
        A wrapper function to execute an INSERT command with psycopg2, with
        added assertions.

        Parameters:
        - cursor: The cursor object from psycopg2 connection
        - table_name: Name of the table to insert data into
        - fields: Tuple or list of field names to insert data into
        - values: Tuple or list of values corresponding to the fields

        Raises:
        - AssertionError: If the number of fields does not match the
                          number of values.

        Returns:
        None

        Usage:
        ```
        execute_insert('students', ('name', 'age'), ('John Doe', 20))
        ```
        """
        assert len(fields) == len(values), "ERROR"

        fields_str = ', '.join(fields)
        placeholders = ', '.join(['%s'] * len(values))
        command = f"""INSERT INTO {table_name}
                        ({fields_str})
                        VALUES ({placeholders});"""

        with self.connection as cursor:
            cursor.execute(command, values)


database_actions = DatabaseActions(DatabaseConnection())
