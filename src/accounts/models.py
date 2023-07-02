from datetime import datetime
from flask_login import UserMixin
from src import bcrypt, db


class User(UserMixin, db.Model):
    """User model to store user details"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(16))
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, email, password, phone_number, created_at, updated_at, is_admin=False):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.phone_number = phone_number
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.is_admin = is_admin

    def __repr__(self):
        return f"<email {self.email}>"
