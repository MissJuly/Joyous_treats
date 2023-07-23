import secrets
from datetime import datetime, timedelta
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_user, login_required, logout_user
from flask_mail import Mail, Message


from src import app, bcrypt, db, mail
from src.accounts.models import User
from src.shop.models import Order, Product
from src.shop.forms import ProductForm

from .forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm


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
        return redirect(url_for("accounts.user_dashboard"))

    # Render the registration template with the form
    return render_template('register.html', form=form)

# Route for user login
@accounts_bp.route("/login", methods=['GET', 'POST'])
def login():
    # Check if the user is already authenticated (logged in)
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("accounts.user_dashboard"))

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
                return redirect(url_for("admin.admin_dashboard"))
            else:
                return redirect(url_for("accounts.user_dashboard"))
        else:
            # If the email and/or password is incorrect, show an error message
            flash("Invalid email and/or password.", "danger")
            return  redirect(url_for("accounts.login"))
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

# Route for user dashboard
@accounts_bp.route("/user")
@login_required
def user_dashboard():
    # Check if the user is logged in
    if current_user.is_authenticated:
        # Retrieve the current user's orders from the database
        user_orders = Order.query.filter_by(user=current_user.id).all()
        return render_template("user.html", user_orders=user_orders)
    else:
        # Redirect the user to the login page if they are not logged in
        return redirect(url_for('accounts.login'))

@accounts_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        email = form.email.data

        # Retrieve the user from the database
        user = User.query.filter_by(email=email).first()

        if user:
            # Generate a unique token
            token = secrets.token_urlsafe(32)

            # Set the token expiration time
            expiration_time = datetime.now() + timedelta(hours=1)

            # Store the token and expiration time in the user object
            user.reset_token = token
            user.reset_token_expiration = expiration_time
            db.session.commit()

            # Send the password reset email with the token
            send_password_reset_email(email, token)

        return "Password reset email sent!"  # Display a success message

    return render_template("reset_forgot_password.html", form=form, reset_mode=False)

def send_password_reset_email(email, token):
    try:
        # Create a password reset URL with the token as a query parameter
        reset_url = url_for("accounts.reset_password", token=token, _external=True)

        # Create the email message
        subject = "Password Reset"
        body = f"Click the following link to reset your password: {reset_url}"
        sender = app.config["MAIL_DEFAULT_SENDER"]
        recipient = email
        message = Message(subject=subject, body=body, sender=sender, recipients=[recipient])

        # Send the email
        mail.send(message)

        # Log successful email sending
        app.logger.info("Password reset email sent successfully to %s", email)
    except Exception as e:
        # Log the error and provide a fallback message
        app.logger.error("Failed to send password reset email to %s. Error: %s", email, str(e))
        raise

@accounts_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    form = ResetPasswordForm()

    if form.validate_on_submit():
        password = form.password.data
        confirm_password = form.confirm_password.data

        # Validate password and confirm_password match

        # Update the user's password in the database
        hashed_password = generate_password_hash(password)

        # Display a success message or redirect to a success page

    return render_template("reset_forgot_password.html", form=form, reset_mode=True, token=token)
