from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import get_db_connection
from .forms import LoginForm, ChangePasswordForm, RegistrationForm, BookingForm
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        email_address = form.email.data
        password = form.password.data

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM User WHERE email_address = %s', (email_address,))
        user = cursor.fetchone()
        conn.close()

        if user is None:
            flash("You are not authorized to login!", "danger")
        elif user['password'] != password:
            flash("Incorrect password!", "danger")
        else:
            session['email_address'] = user['email_address']
            session['user_name'] = user['user_name']
            # Pass the user's name to the home page after successful login
            return redirect(url_for('main.customer_home', user_name=user['user_name'], email_address=user['email_address']))

    return render_template('index.html', form=form)

@main.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        email = form.email.data
        old_password = form.old_password.data
        new_password = form.new_password.data

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if user exists
        cursor.execute('SELECT * FROM User WHERE email_address = %s', (email,))
        user = cursor.fetchone()

        if not user:
            flash("User not found!", "danger")
        elif old_password == new_password:
            flash("New password must be different from the old password!", "danger")
        else:
            # Update password in the database (hashing the new password)
            hashed_password = new_password
            cursor.execute('UPDATE User SET password = %s WHERE email_address = %s', (hashed_password, email))
            conn.commit()
            flash("Password updated successfully!", "success")
            conn.close()
            return redirect(url_for('main.index'))  # Redirect to login page

        conn.close()
    
    else:
        # Flash the error messages for invalid form
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, 'error')  # Flash the error message with category 'error'

    return render_template('change_password.html', form=form)

@main.route('/customer_home')
def customer_home():
    # Get the user's name from the query string or session (if you're using sessions)
    user_name = session.get('user_name')
    
    # Pass the user_name to the template
    return render_template('customer_home.html', user_name=user_name)

from flask import flash, redirect, url_for, render_template
import mysql.connector
from mysql.connector import errors

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Gather form data
        user_name = form.user_name.data
        email = form.email.data
        mobile_number = form.mobile_number.data
        date_of_birth = form.date_of_birth.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        security_question = form.security_question.data
        security_answer = form.security_answer.data

        # Validate form fields
        if not user_name or not email or not mobile_number or not date_of_birth or not password or not security_question or not security_answer:
            flash("All fields are required.", "danger")
            return render_template('register.html', form=form)
        
        # Hash the password (ensure proper hashing, not plain text)
        hashed_password = password  # Note: Implement proper hashing (e.g., using bcrypt)

        try:
            # Insert into database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO User (email_address, user_name, mobile_number, date_of_birth, password, security_question, security_answer, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'user')
            ''', (email, user_name, mobile_number, date_of_birth, hashed_password, security_question, security_answer))

            conn.commit()
            conn.close()

            flash("Registration successful!", "success")
            return redirect(url_for('main.register'))  # Redirect to login page

        except errors.IntegrityError as e:
            # Handle specific error for duplicate entry (email or mobile)
            if "user.PRIMARY" in str(e):  # Check if the error is related to the email field
                flash("Email already exists", "danger")
            elif "user.mobile_number" in str(e):  # Check if the error is related to the mobile number field
                flash("Mobile number already exists", "danger")
            else:
                flash("An error occurred during registration. Please try again.", "danger")
            return render_template('register.html', form=form)

    else:
        # Flash the error messages for invalid form
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, 'error')  # Flash the error message with category 'error'

    return render_template('register.html', form=form)


@main.route('/index')
def redirect_index():
    return redirect(url_for('main.index'))

@main.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    form = BookingForm()
    
    if request.method == 'POST':
        # Retrieve selected movie and theater info
        selected_movie_theater = request.form['movie_theater']
        movie_name, theater_name = selected_movie_theater.split('|')  # Extract movie and theater from the radio button value
        
        # Retrieve date and time for booking
        date_of_booking = form.date_of_booking.data
        time_of_booking = form.time_of_booking.data
        no_of_tickets = form.no_of_tickets_required.data
        
        
        # Convert date_of_booking to string (in YYYY-MM-DD format)
        date_of_booking_str = date_of_booking.strftime('%Y-%m-%d')

        # Fetch seat capacity and price per ticket from the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('''SELECT seat_capacity, price_per_ticket FROM Theater WHERE theater_name = %s''', (theater_name,))
        theater_data = cursor.fetchone()
        
        if not theater_data:
            flash(f"The theater {theater_name} was not found!", "danger")
            return render_template('book_ticket.html', form=form)
        
        seat_capacity = theater_data['seat_capacity']
        price_per_ticket = theater_data['price_per_ticket']
        
        # Calculate available seats
        cursor.execute('''SELECT SUM(no_of_tickets_required) AS booked_tickets
                          FROM Booking
                          WHERE movie_name = %s AND theater_name = %s AND date_of_booking = %s AND time_of_booking = %s''', 
                       (movie_name, theater_name, date_of_booking_str, time_of_booking))
        booked_tickets = cursor.fetchone()['booked_tickets'] or 0
        
        available_seats = seat_capacity - booked_tickets
        if no_of_tickets > available_seats:
            flash(f"Only {available_seats} tickets available.", "danger")
            return render_template('book_ticket.html', form=form)
        
        # Calculate the total amount
        total_amount = no_of_tickets * price_per_ticket
        
        # Insert the booking record into the database
        user_email = session.get('email_address')  # Replace with the actual user's email
        cursor.execute('''INSERT INTO Booking (email_address, movie_name, theater_name, date_of_booking, time_of_booking, 
                                               no_of_tickets_required, total_amount, status)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, 'Booked')''', 
                       (user_email, movie_name, theater_name, date_of_booking_str, time_of_booking, no_of_tickets, total_amount))
        conn.commit()

        new_seat_capacity = seat_capacity - no_of_tickets
        cursor.execute('''UPDATE Theater 
                          SET seat_capacity = %s 
                          WHERE theater_name = %s''', 
                       (new_seat_capacity, theater_name))
        conn.commit()

        conn.close()

        flash("Your booking is confirmed!", "success")
        return redirect(url_for('main.book_ticket'))  # Redirect to home page after booking

    # Fetch movie and theater details for displaying the table
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('''
    SELECT m.movie_name, t.theater_name, m.language, m.category, t.seat_capacity, t.price_per_ticket
    FROM Movie m
    JOIN Schedule s ON m.movie_name = s.movie_name
    JOIN Theater t ON s.theater_name = t.theater_name
    ''')

    movies_theaters = cursor.fetchall()
    conn.close()

    return render_template('customer_book.html', form=form, movies_theaters=movies_theaters)

@main.route('/booking_history', methods=['GET'])
def booking_history():
    # Get the logged-in user's email address
    email_address = session.get('email_address')  # Replace with session-based user email or logged-in user's email

    # Fetch the booking history for the user
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT b.booking_id, b.movie_name, b.theater_name, b.date_of_booking, b.time_of_booking, 
               b.no_of_tickets_required, b.total_amount, b.status
        FROM Booking b
        WHERE b.email_address = %s
        ORDER BY b.date_of_booking DESC
    """, (email_address,))
    
    bookings = cursor.fetchall()
    
    cursor.close()
    connection.close()

    if not bookings:
        flash("No booking history found!")
    
    return render_template('customer_history.html', bookings=bookings)

@main.route('/cancel_ticket', methods=['GET', 'POST'])
def cancel_ticket():
    # Get logged-in user's email from session
    email_address = session.get('email_address')  # Ensure the email is in session
    if not email_address:
        flash("You need to log in to cancel your booking!", "danger")
        return redirect(url_for('main.cancel_ticket'))

    if request.method == 'POST':
        selected_booking_id = request.form.get('selected_booking')  # Get the selected booking ID
        theater_name = request.form.get('theater_name')  # Get the selected theater name from the form
        no_of_tickets_required  = request.form.get('no_of_tickets_required')
        no_of_tickets_required = int(no_of_tickets_required)
        
        if not selected_booking_id:
            flash("Please select at least one of the bookings to cancel", "danger")
            return render_template('customer_cancel.html')

        # Check if the selected booking is valid
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Proceed to cancel the booking
        cursor.execute("""
            UPDATE Booking
            SET status = 'Cancelled'
            WHERE booking_id = %s
        """, (selected_booking_id,))


        conn.commit()

        # Update the theater's seat capacity (add back the canceled tickets)
        cursor.execute("""
            SELECT seat_capacity
            FROM Theater
            WHERE theater_name = %s
        """, (theater_name,))
        theater_data = cursor.fetchone()


        current_seat_capacity = theater_data['seat_capacity']

        # Add back the canceled tickets to the seat capacity
        new_seat_capacity = current_seat_capacity + no_of_tickets_required 

        # Update the seat capacity in the Theater table
        cursor.execute("""
                UPDATE Theater
                SET seat_capacity = %s
                WHERE theater_name = %s
        """, (new_seat_capacity, theater_name))
        conn.commit()

        conn.close()

        flash("Movie ticket cancellation is done successfully!", "success")
        return redirect(url_for('main.cancel_ticket'))  # Redirect to home page after cancellation
    
    email_address = session.get('email_address')  # Replace with session-based user email or logged-in user's email
    # Fetch all bookings of the user which are booked and have a future date
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT b.booking_id, b.movie_name, b.theater_name, b.date_of_booking, b.time_of_booking, 
               b.no_of_tickets_required, b.total_amount, b.status
        FROM Booking b
        WHERE b.email_address = %s AND b.status <> 'Cancelled'
        ORDER BY b.date_of_booking DESC
    """, (email_address,))

    
    bookings = cursor.fetchall()

    conn.close()

    return render_template('customer_cancel.html', bookings=bookings)
