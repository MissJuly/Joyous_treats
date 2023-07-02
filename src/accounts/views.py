from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user

from src import bcrypt, db
from src.accounts.models import User

from .forms import LoginForm, RegisterForm


accounts_bp = Blueprint(
    "accounts", __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path="/accounts/static"
)

@accounts_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You are already registered!")
        return redirect(url_for("core.home"))
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # Gets current timestamp
        current_time = datetime.now()

        user = User(name=form.name.data,
                    email=form.email.data,
                    phone_number=form.phone_number.data,
                    password=form.password.data,
                    created_at=current_time,
                    updated_at=current_time)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("You registered and are now logged in. Welcome!", "success")

        return redirect(url_for("core.home"))

    return render_template('register.html', form=form)

@accounts_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("core.home"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("core.home"))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("accounts.login"))
