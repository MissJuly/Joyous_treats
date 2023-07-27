from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for, json, flash, send_from_directory
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy import or_
from src import db, app
from src.accounts.models import User
from src.shop.forms import ProductForm, SearchForm
from src.shop.models import Product, Order, OrderItem
import os
import stripe


# Create a Blueprint for the shop section of the website
shop_bp = Blueprint(
    "shop", __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path="/shop/static"
)

# Define a route for the main shop page
@shop_bp.route("/shop")
def shop():
    categories = ['cakes', 'pies', 'pastries', 'fancy desserts']
    # category_images = get_category_images(categories)
    return render_template('shop.html', categories=categories, get_category_images=get_category_images, get_category_alt=get_category_alt)

def get_category_images(categories):
    category_images = {
        'cakes': 'cake-1.jpg',
        'pies': 'pie-1.jpg',
        'pastries': 'pastry-1.jpg',
        'fancy desserts': 'fd-1.jpg'
    }
    return [category_images.get(category) for category in categories]

def get_category_alt(category):
    category_alts = {
        'cakes': 'oreo cake',
        'pies': 'mini chocolate pies',
        'pastries': 'croissant',
        'fancy desserts': 'pastel colored macarons'
    }
    return category_alts.get(category, '')

@shop_bp.route("/shop/<category_name>")
def category(category_name):
    products = Product.query.filter_by(category=category_name).all()
    message = get_category_message(category_name)
    return render_template('products.html', category=category_name, products=products, message=message)

def get_category_message(category_name):
    if category_name == 'cakes':
        return 'Take a walk through our cakes and be inspired to try...everything!'
    elif category_name == 'pies':
        return "A world of irresistible pie goodness... don't be shy!!!"
    elif category_name == 'pastries':
        return 'Indulge in a symphony of flavors that will transport you to pastry paradise!!!'
    elif category_name == 'fancy desserts':
        return 'A realm where dessert dreams come true!!!'
    else:
        return ''

#
# Search products in database
@shop_bp.route("/search", methods=['POST', 'GET'])
def search():
    form = SearchForm(request.form)
    if form.validate_on_submit():
        search_term = form.query.data
        # Query the products based on the search term
        products = Product.query.filter(or_(Product.name.ilike(f"%{search_term}%"),
                                            Product.category.ilike(f"%{search_term}%"),
                                            Product.description.ilike(f"%{search_term}%"))).all()
        # Render the search results template with the products
        return render_template('search.html', form=form, products=products, search_term=search_term)
    return render_template('search.html', form=form, products=[], search_term=search_term)


# Route for product detail view
@shop_bp.route('/product-detail/<int:product_id>',  methods=['GET', 'POST'])
@login_required
def product_detail(product_id):
    product = Product.query.get(product_id)
    if request.method == 'POST':
        order_item = OrderItem.query.filter_by(product=product, user=current_user.id, status=False).first()
        order = Order.query.filter_by(user=current_user.id, status=False).first()

        if order:
            # Check if order_item exists
            if order_item:
                order_item.quantity += 1
                order.total_amount = order.calculate_total_amount()
                db.session.commit()
                flash('Product added successfully!', 'success')
                return redirect(url_for('shop.cart'))
            else:
                order = Order.query.filter_by(user=current_user.id, status=False).first()
                order_item = OrderItem(product=product, user=current_user.id, order=order.id)
                db.session.add(order_item)
                order.total_amount = order.calculate_total_amount()
                db.session.commit()
                flash('Product added successfully!', 'success')
                return redirect(url_for('shop.cart'))
        else:
            order = Order(user=current_user.id)
            db.session.add(order)
            new_order = Order.query.filter_by(user=current_user.id, status=False).first()
            order_item = OrderItem(product=product, user=current_user.id, order=new_order.id)
            db.session.add(order_item)
            new_order.total_amount = new_order.calculate_total_amount()
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('shop.cart'))

    return render_template('product-detail.html', product=product)

@shop_bp.route("/delete_item/<int:order_item_id>", methods=["POST"])
def delete_item(order_item_id):
    # Get the order item by its ID and delete it from the cart
    order_item = OrderItem.query.get_or_404(order_item_id)
    db.session.delete(order_item)
    db.session.commit()

    # Redirect to the cart page
    return redirect(url_for("shop.cart"))


@shop_bp.route("/clear_cart", methods=["POST"])
def clear_cart():
    # Retrieve all orders from the cart
    orders = Order.query.all()

    # Delete all associated order items first
    for order in orders:
        order_items = OrderItem.query.filter_by(order=order.id).all()
        for order_item in order_items:
            db.session.delete(order_item)

    # Delete the orders
    for order in orders:
        db.session.delete(order)

    # Commit the changes to the database
    db.session.commit()

    # Redirect to the cart page
    return redirect(url_for("shop.cart"))


@shop_bp.route('/cart')
@login_required
def cart():
    orders = Order.query.filter_by(user=current_user.id, status=False).first()
    return render_template('cart.html', orders=orders)


@shop_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    DOMAIN = 'http://127.0.0.1:5000'
    if request.method == 'POST':
        order = Order.query.filter_by(user=current_user.id, status=False).first()
        price = order.total_amount
        stripe_price = int(price * 100)
        customer_order_id = f'Order ID: #{order.id}'

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'unit_amount': stripe_price,
                            'currency' : 'kes',
                            'product_data' : {
                                'name' : customer_order_id
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=url_for('shop.success', _external=True),
                cancel_url=DOMAIN + '/cancel',
        )
        except Exception as e:
            return str(e)

    return redirect(checkout_session.url, code=303)

@shop_bp.route('/success')
def success():
    return render_template('success.html')

@shop_bp.route('/cancel')
def cancel():
    return render_template('cancel.html')
