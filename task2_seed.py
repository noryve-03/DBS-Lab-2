"""
Seeding library database.

No imports outside the standard library may be used
"""

import random
from datetime import datetime, timedelta

from database_actions import database_actions
import psycopg2

def fetch_existing_student_ids():
    # Assuming you have these details available
    conn_details = {
        "dbname": "library",
        "user": "freeman",
        "password": "5432",
        "host": "localhost"  # or wherever your database is hosted
    }
    conn = psycopg2.connect(**conn_details)
    cur = conn.cursor()
    cur.execute('SELECT student_id FROM student')
    student_ids = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return student_ids

def generate_student_data(num_students):
    student_data = []
    for _ in range(num_students):
        name = f"{random.randint(1, 1000)}"
        # Generate a random enrollment date within the last 10 years
        # enrollment_date = datetime.now() - timedelta(days=random.randint(1, 3650))
        # Generate dummy address data
        _address = f"{random.randint(100, 999)} Main St"
        street = f"{random.randint(100, 999)} Elm St"
        city = "Anytown"
        state = "CA"
        phone_number = f"{random.randint(100, 999)}-555-{random.randint(1000, 9999)}"
        student_data.append((name, _address, street, city, state, phone_number))
    return student_data

def seed():
    """
    Insert data for 3 publishers.
    Add 20 authors.
    Create 200 book entries.
    Tie each book to an edition.
    Register 100 students.
    Record 500 borrow transactions, associating books with students.
    """
    publishers = [
        ('Penguin Random House',), 
        ('HarperCollins',), 
        ('Simon & Schuster',), 
        ('Hachette Book Group',), 
        ('Macmillan Publishers',)
    ]
    for publisher in publishers:
        database_actions.execute_insert('publisher', ['publisher_name'], publisher)
    
    # Add 20 authors
    authors = [
        ('Victor Hugo',), ('Alexandre Dumas',), ('Gustave Flaubert',), 
        ('Emile Zola',), ('Jules Verne',), ('Guy de Maupassant',), 
        ('Charles Baudelaire',), ('Arthur Rimbaud',), ('Paul Verlaine',), 
        ('Marcel Proust',), ('Albert Camus',), ('Jean-Paul Sartre',), 
        ('Simone de Beauvoir',), ('Francois Mauriac',), ('Andre Gide',), 
        ('Antoine de Saint-Exupery',), ('Romain Gary',), ('Marguerite Duras',),  
        ('Colette',), ('Marcel Ayme',)
    ]
    for author in authors:
        database_actions.execute_insert('author', ['name'], author)


    def generate_book(publishers, authors):
        title = f"{random.randint(1, 1000)}"
        publisher = random.choice(publishers)
        author = random.choice(authors) if random.random() < 0.3 else None  # 30% chance of having a listed author
        edition_year = random.randint(1990, 2020)
        return title, publisher, author, edition_year

    books = [generate_book(publishers, authors) for _ in range(200)]
    for book in books:
        title, publisher, author, edition_year = book

        # Insert book
        book_id = database_actions.execute_insert('book', ['title'], (title,))

        # First, insert into book_edition to generate an edition_number

        # Then, use the generated edition_number when inserting into the edition table
        database_actions.execute_insert('edition', ['edition_year', 'book_id'], (edition_year, book_id))

        # If the book has an author, insert into book_author
        # if author:
            # database_actions.execute_insert('book_author', ['book_id', 'author_id'], (book_id, author[0]))

        # Insert into book_publisher
        # database_actions.execute_insert('book_publisher', ['book_id', 'publisher_id'], (book_id, publisher[0]))

    students = generate_student_data(100)
    for student in students:
        database_actions.execute_insert('student', ('student_name', '_address', 'street', 'city', 'state', 'phone_number'), student)


    borrow_transactions = []


    # Fetch existing student IDs
    existing_student_ids = fetch_existing_student_ids()

    # Then, when generating a borrow transaction, select a random student_id from existing_student_ids
    for _ in range(500):
        student_id = random.choice(existing_student_ids)
        # Randomly select a book
        book = random.choice(books)
        
        # Generate a random borrow date within the last 2 years
        borrow_date = datetime.now() - timedelta(days=random.randint(1, 730))
        # Generate a random return date, ensuring it's after the borrow date
        return_date = borrow_date + timedelta(days=random.randint(1, 90))
        due_date = borrow_date + timedelta(days=random.randint(1, 90))
        # Create a transaction tuple
        transaction = (student_id, book[0], borrow_date, return_date)
        borrow_transactions.append(transaction)

    # Insert borrow transactions into the database
    for transaction in borrow_transactions:
        database_actions.execute_insert('borrows', ['student_id', 'book_id', 'check_out_date', 'due_date', 'return_date'], [transaction[0], transaction[1], transaction[2], due_date, transaction[3]])

if __name__ == '__main__':
    seed()
