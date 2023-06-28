from flask import Flask, render_template, url_for, jsonify, json, request
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy import true
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import os
import mysql.connector


app = Flask(__name__)


load_dotenv()  #takes environmental variables from .env

# database configuration settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@<hostname>/{}'.format(os.environ.get("username"), os.environ.get("password"), os.environ.get("database"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecretkey'

db = SQLAlchemy(app)

migrate = Migrate()
migrate.init_app(app, db)


class User(db.Model):
    """User model to store user details"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    created_at = db.Column(db.Datetime)
    updated_at = db.Column(db.Datetime)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User

class Product(db.Model):
    """Product model to store product deatils"""
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    product_category = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    image_url = db.Column(db.String(100))
    availability = db.Column(db.Boolean)
    discount = db.Column(db.Float)
    created_at = db.Column(db.Datetime)
    updated_at = db.Column(db.Datetime)

class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product

# contains several order items
class Order(db.Model):
    """Order model to store order details"""
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_date = db.Column(db.Datetime)
    status = db.Column(db.Boolean)
    total_amount = db.Column(db.Float)
    created_at = db.Column(db.Datetime)
    updated_at = db.Column(db.Datetime)

class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order

class OrderItem(db.Model):
    """Order item model to store order item details"""
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    orderid = db.Column(db.Integer, db.ForeignKey('order.id'))
    productid = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    subtotal = db.Column(db.Float)
    created_at = db.Column(db.Datetime)
    updated_at = db.Column(db.Datetime)

class OrderItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItem

# authentication routes
# User login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    return render_template('login.html')
