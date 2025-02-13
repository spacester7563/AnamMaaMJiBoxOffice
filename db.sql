CREATE DATABASE Movie_Booking;

USE Movie_Booking;

CREATE TABLE User (
    email_address VARCHAR(50) PRIMARY KEY,
    user_name VARCHAR(50) NOT NULL,
    mobile_number BIGINT(10) UNIQUE NOT NULL,
    date_of_birth DATE NOT NULL,
    password VARCHAR(50) NOT NULL,
    security_question VARCHAR(50) NOT NULL,
    security_answer VARCHAR(50) NOT NULL,
    role ENUM('admin', 'tech_admin', 'user') DEFAULT 'user'
) ENGINE=InnoDB;

INSERT INTO User (email_address, user_name, mobile_number, date_of_birth, password, security_question, security_answer, role) 
VALUES ('testuser@example.com', 'Test User', 1234567890, '1990-01-01', 'TestPassword123', 'What is your pet\'s name?', 'Fluffy', 'user');

insert into User (email_address, user_name, mobile_number, date_of_birth, password, security_question, security_answer, role)
values('Raj@gmail.com', 'Raj', 1234567898, '1994-12-02', 'xyz123', 'Where is your favorite place to vacation?', 'Ooty', 'user');

insert into User (email_address, user_name, mobile_number, date_of_birth, password, security_question, security_answer, role)
values('Ram@gmail.com', 'Ram', 234567899, '1990-01-01', 'xyz124', 'What was the name of your favorite pet?', 'Dog', 'user');

insert into User (email_address, user_name, mobile_number, date_of_birth, password, security_question, security_answer, role)
values('Mary@gmail.com', 'Mary', 1234567891, '1990-12-08', 'xyz128', 'What was the name of your favorite pet?', 'Cat', 'user');

insert into User (email_address, user_name, mobile_number, date_of_birth, password, security_question, security_answer, role)
values('Sham@gmail.com', 'Sham', 1234567896, '1990-12-12', 'xyz125', 'What is your favorite food?', 'Chicken', 'admin');

insert into User (email_address, user_name, mobile_number, date_of_birth, password, security_question, security_answer, role)
values('balaji123@gmail.com', 'Balaji', 9834567891, '1992-01-18', 'bal128', 'What was the name of your favorite pet?', 'Cat', 'admin');

insert into User (email_address, user_name, mobile_number, date_of_birth, password, security_question, security_answer, role)
values('Peter@gmail.com', 'Peter', 1234567894, '1990-03-14', 'xyz126', 'What city were you born in?', 'Bangalore', 'tech_admin');

insert into User (email_address, user_name, mobile_number, date_of_birth, password, security_question, security_answer, role)
values('John@gmail.com', 'John', 1234567892, '1990-07-23', 'xyz127', 'Where is your favorite place to vacation?', 'Mysore', 'tech_admin');

insert into User (email_address, user_name, mobile_number, date_of_birth, password, security_question, security_answer, role)
values('alice@gmail.com', 'Alice', 9876543210, '1992-02-15', 'alice123', 'What is your mother\'s maiden name?', 'Smith', 'user');

insert into User (email_address, user_name, mobile_number, date_of_birth, password, security_question, security_answer, role)
values('bob@gmail.com', 'Bob', 9876543211, '1991-09-10', 'bob123', 'What was the name of your first school?', 'Sunshine School', 'user');

insert into User (email_address, user_name, mobile_number, date_of_birth, password, security_question, security_answer, role)
values('charlie@gmail.com', 'Charlie', 9876543212, '1989-06-22', 'charlie123', 'What is your favorite color?', 'Blue', 'user');

insert into User (email_address, user_name, mobile_number, date_of_birth, password, security_question, security_answer, role)
values('diana@gmail.com', 'Diana', 9876543213, '1993-11-05', 'diana123', 'What is your father\'s name?', 'John', 'user');

insert into User (email_address, user_name, mobile_number, date_of_birth, password, security_question, security_answer, role)
values('elizabeth@gmail.com', 'Elizabeth', 9876543214, '1990-05-18', 'elizabeth123', 'Where were you born?', 'London', 'user');

insert into User (email_address, user_name, mobile_number, date_of_birth, password, security_question, security_answer, role)
values('frank@gmail.com', 'Frank', 9876543215, '1988-08-29', 'frank123', 'What is your favorite movie?', 'Inception', 'user');


CREATE TABLE Movie (
    movie_name VARCHAR(50) PRIMARY KEY,
    language ENUM('English', 'Hindi', 'Kannada', 'Tamil', 'Telugu', 'Malayalam') NOT NULL,
    category ENUM('Comedy', 'Action', 'Horror') NOT NULL,
    release_date DATE NOT NULL
) ENGINE=InnoDB;

-- Inserting test data into the Movie table
INSERT INTO Movie (movie_name, language, category, release_date)
VALUES ('DDL', 'Hindi', 'Action', '2020-12-10');

INSERT INTO Movie (movie_name, language, category, release_date)
VALUES ('Bahubali', 'Tamil', 'Horror', '2020-10-13');

INSERT INTO Movie (movie_name, language, category, release_date)
VALUES ('Dhoom', 'Telugu', 'Comedy', '2020-12-14');

INSERT INTO Movie (movie_name, language, category, release_date)
VALUES ('Gangster', 'Kannada', 'Action', '2020-12-15');

INSERT INTO Movie (movie_name, language, category, release_date)
VALUES ('Penguin', 'Malayalam', 'Action', '2020-10-15');

CREATE TABLE Theater (
    theater_name VARCHAR(50) PRIMARY KEY,
    owner_email VARCHAR(50) NOT NULL,
    show_time VARCHAR(50) DEFAULT '10AM to 1PM, 2PM to 5PM, 6PM to 9PM' NOT NULL,
    seat_capacity INT NOT NULL,
    price_per_ticket FLOAT NOT NULL,
    FOREIGN KEY (owner_email) REFERENCES User(email_address)
) ENGINE='InnoDB';

-- Inserting data into Theater table
INSERT INTO Theater (theater_name, owner_email, seat_capacity, price_per_ticket)
VALUES ('Nataraj', 'Ram@gmail.com', 100, 100);

INSERT INTO Theater (theater_name, owner_email, seat_capacity, price_per_ticket)
VALUES ('Rocky', 'Peter@gmail.com', 100, 200);

INSERT INTO Theater (theater_name, owner_email, seat_capacity, price_per_ticket)
VALUES ('Madhubala', 'John@gmail.com', 100, 300);

INSERT INTO Theater (theater_name, owner_email, seat_capacity, price_per_ticket)
VALUES ('Star', 'Ram@gmail.com', 100, 400);

INSERT INTO Theater (theater_name, owner_email, seat_capacity, price_per_ticket)
VALUES ('C3Cinema', 'Peter@gmail.com', 100, 400);

CREATE TABLE Schedule (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    theater_name VARCHAR(50) NOT NULL,
    movie_name VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    FOREIGN KEY (theater_name) REFERENCES Theater(theater_name),
    FOREIGN KEY (movie_name) REFERENCES Movie(movie_name)
) ENGINE=InnoDB AUTO_INCREMENT=101;

-- Inserting data into Schedule table
INSERT INTO Schedule (theater_name, movie_name, start_date, end_date)
VALUES ('Nataraj', 'DDL', '2023-02-10', '2023-02-24');

INSERT INTO Schedule (theater_name, movie_name, start_date, end_date)
VALUES ('Rocky', 'Dhoom', '2023-02-11', '2023-02-25');

INSERT INTO Schedule (theater_name, movie_name, start_date, end_date)
VALUES ('Madhubala', 'Bahubali', '2023-01-13', '2023-02-01');

INSERT INTO Schedule (theater_name, movie_name, start_date, end_date)
VALUES ('Star', 'Penguin', '2023-01-25', '2023-02-12');

INSERT INTO Schedule (theater_name, movie_name, start_date, end_date)
VALUES ('C3Cinema', 'DDL', '2023-01-13', '2023-02-01');


CREATE TABLE Booking (
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    email_address VARCHAR(50) NOT NULL,
    movie_name VARCHAR(50) NOT NULL,
    theater_name VARCHAR(50) NOT NULL,
    date_of_booking DATE NOT NULL,
    time_of_booking VARCHAR(30) NOT NULL,
    no_of_tickets_required INT NOT NULL,
    total_amount FLOAT NOT NULL DEFAULT 0.0,
    status ENUM('Booked', 'Cancelled') NOT NULL,
    FOREIGN KEY (email_address) REFERENCES User(email_address),
    FOREIGN KEY (movie_name) REFERENCES Movie(movie_name),
    FOREIGN KEY (theater_name) REFERENCES Theater(theater_name)
) ENGINE='InnoDB' AUTO_INCREMENT=2001;

-- Inserting data into Booking table
INSERT INTO Booking (email_address, movie_name, theater_name, date_of_booking, time_of_booking, no_of_tickets_required, total_amount, status)
VALUES ('Mary@gmail.com', 'DDL', 'Nataraj', '2023-02-21', '10AM to 1PM', 4, 400, 'Booked');

INSERT INTO Booking (email_address, movie_name, theater_name, date_of_booking, time_of_booking, no_of_tickets_required, total_amount, status)
VALUES ('Raj@gmail.com', 'Dhoom', 'Rocky', '2023-02-25', '10AM to 1PM', 4, 800, 'Booked');

INSERT INTO Booking (email_address, movie_name, theater_name, date_of_booking, time_of_booking, no_of_tickets_required, total_amount, status)
VALUES ('Mary@gmail.com', 'DDL', 'C3Cinema', '2023-01-25', '10AM to 1PM', 8, 3200, 'Booked');

INSERT INTO Booking (email_address, movie_name, theater_name, date_of_booking, time_of_booking, no_of_tickets_required, total_amount, status)
VALUES ('Raj@gmail.com', 'Penguin', 'Star', '2023-02-10', '10AM to 1PM', 3, 1200, 'Cancelled');
