-- TODO: DEFINE SCHEMA FOR THE DATABASE 

-- create table book_edition 
-- (edition_number serial primary key);

create table book (
    book_id serial primary key,
    title varchar(255) not null
); 

create table edition (
    edition_number serial primary key,
    edition_year integer not null,
    book_id integer references book(book_id)
);

create table author (
    author_id serial primary key,
    name varchar(255) not null
);

create table book_author (
    book_id integer references book(book_id),
    author_id integer references author(author_id)
);
 
create table publisher (
    publisher_id serial primary key,
    publisher_name varchar(255) not null
);

create table student (
    student_id serial primary key,
    student_name varchar(255) not null,
    _address text not null,
    street varchar(255) not null,
    city varchar(255) not null,
    state varchar(255) not null,
    phone_number varchar(50)
);

create table book_publisher (
    book_id int references book(book_id),
    publisher_id int references publisher(publisher_id)
);

create table borrows (
    student_id integer references student(student_id),
    book_id integer references book(book_id),
    check_out_date date not null,
    due_date date not null,
    return_date date
);

CREATE TABLE IF NOT EXISTS fines (
fine_id SERIAL PRIMARY KEY,
student_id INT NOT NULL,
book_id INT NOT NULL,
days_overdue INT NOT NULL,
fine_amount DECIMAL(10, 2) NOT NULL,
FOREIGN KEY (student_id) REFERENCES student(student_id),
FOREIGN KEY (book_id) REFERENCES book(book_id)
);
