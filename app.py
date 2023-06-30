from flask import Flask, render_template, url_for, jsonify, json, request, redirect
from datetime import datetime, timedelta, timezone, date
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from sqlalchemy import true
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from werkzeug.security import generate_password_hash, check_password_hash
import os
import mysql.connector


app = Flask(__name__)


load_dotenv()  #takes environmental variables from .env

# database configuration settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@localhost/{}'.format(os.environ.get("username"), os.environ.get("password"), os.environ.get("database"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecretkey'

db = SQLAlchemy(app)

migrate = Migrate()
migrate.init_app(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"


class User(db.Model, UserMixin):
    """User model to store user details"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.Date)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


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
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.Date)

class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product

# contains several order items
class Order(db.Model):
    """Order model to store order details"""
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_date = db.Column(db.Date)
    status = db.Column(db.Boolean)
    total_amount = db.Column(db.Float)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.Date)

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
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.Date)

class OrderItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItem

# reloads user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# User login endpoint
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.verify_password(password):
            login_user(user)
            return redirect("/")
        else:
            return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')

# User registration endpoint
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone_number = request.form['phone_number']

        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email already exists')

        user = User(name=name, email=email, phone_number=phone_number)
        user.password = password
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template('register.html')

# Search for product endpoint
@app.route("/api/search", methods=['GET'])
def search():
    keyword = request.args.get('keyword')

    results = []

    if keyword:
        # Perfoems the search based on the keyword using SQLAlchemy query
        products = Product.query.filter(Product.name.ilike('%{}%'.format(keyword))).all()

        # Serializes the products using ProductSchema
        product_schema = ProductSchema(many=True)
        results = product_schema.dump(products)

    return jsonify(results)



# non-authentication routes
@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/shop")
def shop():
    return render_template('shop.html')

@app.route("/shop/cakes")
def cakes():
    return render_template('cakes.html')

@app.route("/shop/pies")
def pies():
    return render_template('pies.html')

@app.route("/shop/pastries")
def pastries():
    return render_template('pastries.html')

@app.route("/shop/fancy-desserts")
def fancy_desserts():
    return render_template('fancy-desserts.html')


if __name__ == "__main__":
    with app.app_context():
        #db.create_all()
        app.run(host='0.0.0.0', debug=True)
