import os
from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_user, login_required, logout_user
from functools import wraps
from werkzeug.utils import secure_filename
# from werkzeug.datastructures import FileStorage

from src import bcrypt, db, images
from src.accounts import views
from src.accounts.models import User
from src.shop.models import Order, Product
from src.shop.forms import ProductForm


def fetch_registered_users():
    # Use SQLAlchemy query to fetch all registered users from database
    users = User.query.all()
    return users

# def fetch_order():
#     # Use SQLAlchemy query to fetch all orders from the databse
#     orders = Order.query.all()
#     return orders

def fetch_available_products():
    # Use SQLAlchemy query to fetch all available products from database
    products = Product.query.all()
    return products

# Create a Blueprint for the admin module
admin_bp = Blueprint(
    "admin", __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path="/admin/static"
)

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
@admin_bp.route("/admin", methods=['GET', 'POST'])
@admin_required
def admin_dashboard():
    users = fetch_registered_users()
    # orders = fetch_order()
    products = fetch_available_products()
    categories = set(product.category for product in products)


    form = ProductForm()

    # print(request.files)
    # print(request.form)
    if form.validate_on_submit():
        # Save the uploaded image file
        filename = secure_filename(form.image.data.filename)
        saved_filename = images.save(form.image.data)

        # Get current timestamp
        current_time = datetime.now()

        # Create a new Product instance
        product = Product(
            name=form.name.data,
            category=form.category.data,
            description=form.description.data,
            price=form.price.data,
            image=saved_filename,
            availability=True,
            discount=form.discount.data,
            created_at=current_time,
            updated_at=current_time
        )

        # Add the new product to the database
        db.session.add(product)
        db.session.commit()

        flash("Product added successfully!", "success")
        return redirect(url_for("admin.admin_dashboard"))
    else:
        print(form.errors)

    return render_template('admin.html', users=users, products=products, categories=categories, form=form)


@admin_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for("admin.admin_dashboard"))

    return render_template('edit_product.html', form=form, product=product)


@admin_bp.route('/delete/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    # Delete the product from the database
    db.session.delete(product)
    db.session.commit()

    flash("Product deleted successfully!", "success")
    return redirect(url_for("admin.admin_dashboard"))
