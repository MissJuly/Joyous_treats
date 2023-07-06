from decouple import config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


# Create a Flask application instance
app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

# Initialize the LoginManager extension to handle user authentication
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize the Bcrypt extension to handle password hashing and checking
bcrypt = Bcrypt(app)

# Initialize the SQLALchemy extension to work with the database
db = SQLAlchemy(app)

# Initialize the Migrate extension to handle database migrations
migrate = Migrate(app, db)

# Registering blueprints for different parts of the application
from src.accounts.views import accounts_bp
from src.admin.views import admin_bp
from src.core.views import core_bp
from src.shop.views import shop_bp


app.register_blueprint(accounts_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(core_bp)
app.register_blueprint(shop_bp)

# Import the User model from accounts module
from src.accounts.models import User

# Import the Product model from shop module
from src.shop.models import Product

# Define a function to load a user based on its user_id
@login_manager.user_loader
def load_user(user_id):
    # Query the User model to get the user with the provided user_id
    return User.query.filter(User.id == int(user_id)).first()

# Set the login view, which redirects to for when a user attempts to access a protected route
login_manager.login_view = "accounts.login"

# Set the flash message category for login message
login_manager.login_message_category = "danger"
