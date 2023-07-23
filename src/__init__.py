from decouple import config
from flask import Flask, send_from_directory
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import CSRFProtect
import os
import stripe
import pymysql
pymysql.install_as_MySQLdb()


# Create a Flask application instance
app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

# COnfigure mail settings
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
app.config["UPLOADED_IMAGES_DEST"] = 'static/images'

# Initialize stripe configuration
stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")
stripe.api_key = stripe_secret_key
app.config["STRIPE_PUBLISHABLE_KEY"] = os.getenv("STRIPE_PUBLISHABLE_KEY")

# Initialize the images upload
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

app.use_static_loader = True

# Initialize the LoginManager extension to handle user authentication
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize the Bcrypt extension to handle password hashing and checking
bcrypt = Bcrypt(app)

# Initialize the SQLALchemy extension to work with the database
db = SQLAlchemy(app)

# Initialize Flask-Mail
mail = Mail(app)

# Initialize the Migrate extension to handle database migrations
migrate = Migrate(app, db)

# Initializes the CSRF protection required for secure form submissions
csrf = CSRFProtect(app)

# Registering blueprints for different parts of the application
from src.accounts.views import accounts_bp
from src.admin.views import admin_bp
from src.core.views import core_bp
from src.shop.views import shop_bp
from src.shop.forms import SearchForm


app.register_blueprint(accounts_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(core_bp)
app.register_blueprint(shop_bp)

# Import the User model from accounts module
from src.accounts.models import User

# Define a function to load a user based on its user_id
@login_manager.user_loader
def load_user(user_id):
    # Query the User model to get the user with the provided user_id
    return User.query.filter(User.id == int(user_id)).first()

# Set the login view, which redirects to for when a user attempts to access a protected route
login_manager.login_view = "accounts.login"

# Set the flash message category for login message
login_manager.login_message_category = "danger"

@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route('/images/<filename>')
def display_images(filename):
    return send_from_directory(app.config["UPLOADED_IMAGES_DEST"], filename)
