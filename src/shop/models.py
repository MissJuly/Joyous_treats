from datetime import datetime
from src import db
from src.accounts.models import User


# Define the Product model class, inheriting from db.Model
class Product(db.Model):
    """Product model to store product details"""

    # Set the table name in the database
    __tablename__ = 'products'

    # Define columns of the 'products' table with their respective data types and constraints
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200))
    availability = db.Column(db.Boolean, default=True)
    discount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    # Constructor for the Product class, initializing its attributes
    def __init__(self, name, category, description, price, created_at, updated_at, image_url=None, availability=True, discount=0.0):
        self.name = name
        self.category = category
        self.description = description
        self.price = price
        self.image_url = image_url
        self.availability = availability
        self.discount = discount
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    # Represent the Product object as a string for debugging and logging purposes
    def __repr__(self):
        return f"<Product {self.id}: {self.name}>"

# Define Order model class for several order items
class Order(db.Model):
    """Order model to store order details"""
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_date = db.Column(db.Date)
    status = db.Column(db.Boolean)
    total_amount = db.Column(db.Float)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.Date)



class OrderItem(db.Model):
    """Order item model to store order item details"""
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer)
    subtotal = db.Column(db.Float)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.Date)
