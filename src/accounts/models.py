from datetime import datetime
from flask_login import UserMixin
from src import bcrypt, db


# Define the User model class, inheriting from UserMixin and db.Model
class User(UserMixin, db.Model):
    """User model to store user details"""

    # Set the table name in the database
    __tablename__ = 'users'

    # Define columns of the 'users' table with their respective data types and constraints
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(16))
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

     # Constructor for the User class, initializing its attributes
    def __init__(self, name, email, password, phone_number, created_at, updated_at, is_admin=False):
        # Set the provided attributes
        self.name = name
        self.email = email
        # Hash the provided password using bcrypt before storing it
        self.password = bcrypt.generate_password_hash(password)
        self.phone_number = phone_number
        # Set the 'created_at' and 'updated_at' attributes to the current datetime
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        # Set the 'is_admin' attribute based pn the provided value (default is False)
        self.is_admin = is_admin

    # Represent the User object as a string for debugging and logging purposes
    def __repr__(self):
        return f"<email {self.email}>"
