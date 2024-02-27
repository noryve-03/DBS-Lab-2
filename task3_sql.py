"""
Each task is a function that returns the result of a SQL query.

No imports outside the standard library may be used
"""
from database_actions import database_actions
from database_connection import DatabaseConnection


def task_3_1():
    """
    List the top 5 most borrowed books in the library.

    The result should include the books title and number of times borrowed, 
    ranked from most borrowed to least borrowed.
    """
    query = """
    SELECT b.title, COUNT(*) AS times_borrowed
    FROM borrows br
    JOIN book b ON br.book_id = b.book_id
    GROUP BY b.title
    ORDER BY times_borrowed DESC
    LIMIT 5
    """
    with DatabaseConnection() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def task_3_2():
    """
    For each month, calculate the total number of books borrowed and the
    average duration (in days) of a borrow.

    - If a book has not been returned yet, it should not be included in
    the average duration.
    - If a book was borrowed in month X and returned in month Y, it should
    be included in the month it was checked out.

    Display the months in a year-month format (YYYY-MM) and order
    by the month ascending.
    """
    query = """
    SELECT 
        TO_CHAR(borrow_date, 'YYYY-MM') AS month,
        COUNT(*) AS total_borrowed,
        AVG(EXTRACT(DAY FROM (return_date - borrow_date))) AS avg_duration
    FROM 
        borrows
    WHERE 
        return_date IS NOT NULL
    GROUP BY 
        month
    ORDER BY 
        month ASC
    """
    with DatabaseConnection() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result

def task_3_3():
    """
    Identify publishers that frequently collaborate with specific authors,
    where "frequent collaboration" means publishers that have published more
    than three books by the same author.
    """
    query = """
    SELECT p.publisher_name, a.name, COUNT(*) AS books_published
    FROM book_publisher bp
    JOIN publisher p ON bp.publisher_id = p.publisher_id
    JOIN book_author ba ON bp.book_id = ba.book_id
    JOIN author a ON ba.author_id = a.author_id
    GROUP BY p.publisher_name, a.name
    HAVING COUNT(*) > 3
    """
    with DatabaseConnection() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result


if __name__ == '__main__':
    pass
