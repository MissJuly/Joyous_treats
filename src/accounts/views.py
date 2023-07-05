from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_user, login_required, logout_user
from functools import wraps

from src import bcrypt, db
from src.accounts.models import User
from src.shop.models import Order, Product
from src.shop.forms import ProductForm

from .forms import LoginForm, RegisterForm



def fetch_registered_users():
    # Use SQLAlchemy query to fetch all registered users from database
    users = User.query.all()
    return users

# def fetch_order():
#     # Use SQLAlchemy query to fetch all orders from the databse
#     orders = Order.query.all()
#     return orders

# Create a Blueprint for the accounts module
accounts_bp = Blueprint(
    "accounts", __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path="/accounts/static"
)

# Route for the user registration
@accounts_bp.route("/register", methods=['GET', 'POST'])
def register():
    # Check if the user is already authenticated (logged in)
    if current_user.is_authenticated:
        flash("You are already registered!")
        return redirect(url_for("core.home"))

    # Create a form object from the RegisterForm class
    form = RegisterForm(request.form)

    # Check if the form has been submitted and is valid
    if form.validate_on_submit():
        # Get current timestamp
        current_time = datetime.now()

        # Create a new User object with the data from the form
        user = User(name=form.name.data,
                    email=form.email.data,
                    phone_number=form.phone_number.data,
                    password=form.password.data,
                    created_at=current_time,
                    updated_at=current_time)

        # Add the new user to the database and commit the changes
        db.session.add(user)
        db.session.commit()

        # Log in the newly registered user
        login_user(user)
        flash("You registered and are now logged in. Welcome!", "success")

        # Redirect the user to the homepage
        return redirect(url_for("core.home"))

    # Render the registration template with the form
    return render_template('register.html', form=form)

# Route for user login
@accounts_bp.route("/login", methods=['GET', 'POST'])
def login():
    # Check if the user is already authenticated (logged in)
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("core.home"))

    # Create a form object from the LoginForm class
    form = LoginForm(request.form)

    # Check if the form has been submitted and is valid
    if form.validate_on_submit():
        # Query the database for the user with the given email
        user = User.query.filter_by(email=form.email.data).first()

        # Check if the user exists and the password is correct
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            # Log in the user
            login_user(user)

            # Set custom session variable
            session["user_id"] = user.id

            # Redirect the user to the appropriate page
            flash("Login successful!", "success")
            if user.is_admin:
                return redirect(url_for("accounts.admin_dashboard"))
            else:
                return redirect(url_for("core.home"))
        else:
            # If the email and/or password is incorrect, show an error message
            flash("Invalid email and/or password.", "danger")
            return render_template('login.html', form=form)

    # Render the login template with the form
    return render_template('login.html', form=form)

# Route for user logout
@accounts_bp.route("/logout")
@login_required
def logout():
    # Log out the user
    logout_user()
    # Show a success message
    flash("You were logged out.", "success")
    # Redirect the user to the login page
    return redirect(url_for("accounts.login"))


# Create custom Admin decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        if user_id != None:
            user = User.query.get(user_id)
            if user.is_admin:
                return f(*args, **kwargs)
            flash("You need admin privileges to access this page", "danger")
            return redirect(url_for("core.home"))

        # flash("Please log in as an admin to access this page!", "danger")
        return redirect(url_for("accounts.login"))
    return decorated_function

# Define route for admin dashboard
@accounts_bp.route("/admin", methods=['GET', 'POST'])
@admin_required
def admin_dashboard():
    users = fetch_registered_users()
    # orders = fetch_order()

    form = ProductForm()

    if form.validate_on_submit():
          # Get current timestamp
         current_time = datetime.now()

        # Process the form data
         product = Product(product_name=form.product_name.data,
                    category=form.category.data,
                    description=form.description.data,
                    price=form.price.data,
                    image_url=form.image_url.data,
                    availability=form.availability.data,
                    discount=form.discount.data,
                    created_at=current_time,
                    updated_at=current_time)

         db.session.add(product)
         db.session.commit()

         flash("Product added successfully!", "success")
         return redirect(url_for("shop.shop"))

    return render_template('admin.html', users=users, form=form)


