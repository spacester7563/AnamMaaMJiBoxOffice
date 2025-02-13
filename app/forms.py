from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, TelField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError, InputRequired, NumberRange
from datetime import datetime

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ChangePasswordForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    old_password = PasswordField('Old Password', validators=[InputRequired()])
    new_password = PasswordField('New Password', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('new_password')])
    submit = SubmitField('SUBMIT')

class RegistrationForm(FlaskForm):
    user_name = StringField('Username', validators=[
        DataRequired(), 
        Length(min=10, max=20), 
        Regexp('^[A-Za-z]*$', message="Username should only contain alphabets.")
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(message="Invalid email address.")
    ])
    mobile_number = TelField('Mobile Number', validators=[
        DataRequired(), 
        Length(min=10, max=10, message="Mobile number must be 10 digits."),
        Regexp('^[0-9]{10}$', message="Invalid mobile number.")
    ])
    date_of_birth = DateField('Date of Birth (MM-DD-YYYY)', format='%m-%d-%Y', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
        Regexp(r'[A-Z]', message="Password must contain at least one uppercase letter."),
        Regexp(r'[0-9]', message="Password must contain at least one digit."),
        Regexp(r'[!@#$%^&*(),.?":{}|<>]', message="Password must contain at least one special character.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password', message="Passwords must match.")])
    
    security_question = SelectField('Security Question', choices=[
        ('', 'Choose a question'), 
        ('favorite_book', 'What is your favorite book?'),
        ('favorite_pet', 'What was the name of your favorite pet?'),
        ('favorite_food', 'What is your favorite food?')
    ], validators=[DataRequired()])
    
    security_answer = StringField('Security Answer', validators=[
        DataRequired(),
        Length(max=20, message="Security answer should not exceed 20 characters."),
        Regexp(r'^[A-Za-z ]*$', message="Security answer can only contain alphabets and spaces.")
    ])
    
    submit = SubmitField('SIGNUP')
    
    # Custom validators
    def validate_email(self, email):
        from .models import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM User WHERE email_address = %s', (email.data,))
        user = cursor.fetchone()
        if user:
            raise ValidationError("Email already exists.")
        conn.close()

    def validate_mobile_number(self, mobile_number):
        from .models import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM User WHERE mobile_number = %s', (mobile_number.data,))
        user = cursor.fetchone()
        if user:
            raise ValidationError("Mobile number already exists.")
        conn.close()



class BookingForm(FlaskForm):
    # Movie name (non-editable)
    movie_name = StringField('Movie Name', validators=[DataRequired()])
    
    # Theater name (non-editable)
    theater_name = StringField('Theater Name', validators=[DataRequired()])
    
    # Language (non-editable)
    language = StringField('Language', validators=[DataRequired()])
    
    # Category (non-editable)
    category = StringField('Category', validators=[DataRequired()])
    
    # Seat capacity (non-editable)
    seat_capacity = IntegerField('Seat Capacity', validators=[DataRequired()])
    
    # Price (non-editable)
    price_per_ticket = IntegerField('Price per Ticket', validators=[DataRequired()])
    
    # Booking Date (editable)
    date_of_booking = DateField('Date of Booking', format='%m-%d-%Y', validators=[DataRequired()])
    
    # Time of Booking (editable)
    time_of_booking = SelectField('Select Time', choices=[
        ('10:00AM to 1:00PM', '10:00AM to 1:00PM'),
        ('02:00PM to 05:00PM', '02:00PM to 05:00PM'),
        ('06:00PM to 09:00PM', '06:00PM to 09:00PM')
    ], validators=[DataRequired()])
    
    # No. of tickets (editable)
    no_of_tickets_required = IntegerField('No. of Tickets', validators=[
        DataRequired(),
        NumberRange(min=1, max=100)
    ])
    
    # Submit button
    submit = SubmitField('Book Now')
    
    def validate_date(self):
        # Booking date must be greater than the current date and within a span of 3 days
        current_date = datetime.now().date()
        if self.date_of_booking.data <= current_date:
            raise ValidationError("Booking date must be greater than the current date.")
        
        if self.date_of_booking.data > current_date + timedelta(days=3):
            raise ValidationError("Booking date must be within 3 days from today.")
    
    def validate_ticket_availability(self, seat_capacity, booked_tickets):
        # Seat capacity check
        available_seats = seat_capacity - booked_tickets
        if self.no_of_tickets_required.data > available_seats:
            raise ValidationError(f"Only {available_seats} seats available.")
