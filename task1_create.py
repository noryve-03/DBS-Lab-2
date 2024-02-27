"""
Execute the script schema.sql to create the database schema.

No imports outside the standard library may be used
"""
from database_actions import database_actions


def task1():
    """
    Execute the schema.sql file to create the database schema.
    """
    # no need to implement anything here
    database_actions.execute_file('schema.sql')


if __name__ == '__main__':
    task1()
