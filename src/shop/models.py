from datetime import datetime
from src import db
from src.accounts.models import User


# Define the Product model class, inheriting from db.Model
class Product(db.Model):
    """Product model to store product details"""

    # Set the table name in the database
    __tablename__ = 'product'

    # Define columns of the 'products' table with their respective data types and constraints
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(250))
    availability = db.Column(db.Boolean, default=False)
    discount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    order_item = db.relationship("OrderItem", backref='orderItem_product')

    # Constructor for the Product class, initializing its attributes
    def __init__(self, name, category, description, price, created_at, updated_at, image=None, availability=True, discount=0.0):
        self.name = name
        self.category = category
        self.description = description
        self.price = price
        self.image = image
        self.availability = availability
        self.discount = discount
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    # Represent the Product object as a string for debugging and logging purposes
    def __repr__(self):
        return f"<Product {self.id}: {self.name}>"

class OrderItem(db.Model):
    """Order item model to store order item details"""
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    product = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, default=1)
    status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.Date, default=datetime.now())
    updated_at = db.Column(db.Date, default=datetime.now())
    order = db.Column(db.Integer, db.ForeignKey('order.id'))


    def __init__(self, user, product, order, quantity=1, status=False):
        self.user = user
        self.product = product
        self.quantity = quantity
        self.status = status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.order = order


    def get_product_price(self):
        return self.quantity * self.product.price

    def __repr__(self):
        return f"<OrderItem {self.id}>"


# Define Order model class for several order items
class Order(db.Model):
    """Order model to store order details"""
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_date = db.Column(db.Date)
    status = db.Column(db.Boolean, default=False)
    total_amount = db.Column(db.Float)
    created_at = db.Column(db.Date, default=datetime.now())
    updated_at = db.Column(db.Date, default=datetime.now())
    order_item = db.relationship('OrderItem', backref='orderItem_orders')


    def __init__(self, user, order_date=None, status=False, total_amount=0.0):
        self.user = user
        self.order_date = order_date
        self.status = status
        self.total_amount = total_amount
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __repr__(self):
        return f"<Order {self.id}>"



