from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for, json, flash
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy import or_
from src import db
from src.accounts.models import User
from src.shop.forms import ProductForm, SearchForm
from src.shop.models import Product, Order, OrderItem



# Create a Blueprint for the shop section of the website
shop_bp = Blueprint(
    "shop", __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path="/shop/static"
)
# Pass to base


# Define a route for the main shop page
@shop_bp.route("/shop")
def shop():
    return render_template('shop.html')

# Define a route for the cakes page
@shop_bp.route("/shop/cakes")
def cakes():
    products = Product.query.filter_by(category='cakes').all()
    return render_template('cakes.html', products=products)

# Define a route for the pies page
@shop_bp.route("/shop/pies")
def pies():
    products = Product.query.filter_by(category='pies').all()
    return render_template('pies.html', products=products)

# Define a route for the pastries page
@shop_bp.route("/shop/pastries")
def pastries():
    products = Product.query.filter_by(category='pastries').all()
    return render_template('pastries.html', products=products)

# Define a route for the fancy desserts page
@shop_bp.route("/shop/fancy-desserts")
def fancy_desserts():
    products = Product.query.filter_by(category='fancy desserts').all()
    return render_template('fancy-desserts.html', products=products)

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


# Api routes
# Retrieve a list of available bakery products
@shop_bp.route("/api/products", methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = []

    for product in products:
        product_data = {
            'id': product.id,
            'name': product.name,
            'category': product.category,
            'description': product.description,
            'price': product.price,
            'image_url': product.image_url,
            'availability': product.availability,
            'discount': product.discount
        }
        product_list.shop_bpend(product_data)

    return jsonify(product_list)

# Fetch details about a specific product by providing its unique identifier
@shop_bp.route("/api/products/<int:product_id>", methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)

    if product is None:
        return jsonify({'error': 'Product not found'}), 404

    product_data = {
            'id': product.id,
            'name': product.name,
            'category': product.category,
            'description': product.description,
            'price': product.price,
            'image_url': product.image_url,
            'availability': product.availability,
            'discount': product.discount
    }

    return jsonify(product_data)

# Route for product detail view
@shop_bp.route('/product-detail/<int:product_id>',  methods=['GET', 'POST'])
def product_detail(product_id):
    product = Product.query.get(product_id)

    if request.method == 'POST':
        # def add_to_cart():
        product = Product.query.get_or_404(product_id)
        user_id = current_user.id
        order_item = OrderItem.query.filter_by(product_id=product.id, user_id=user_id, status=False).first()
        order = Order.query.filter_by(user_id=user_id, status=False).first()

        if order:
            # Check if the order_item is in the order
            if order_item:
                order_item.quantity += 1
                db.session.commit()
                flash("This product quantity was updated", 'success')
                return redirect(url_for('shop.cart'))
            else:
                order_item = OrderItem(product_id=product.id, user_id=user_id)
                db.session.add(order_item)
                order_item.order = order
                db.session.commit()
                flash('This product was added to your cart', 'success')
                return redirect(url_for('shop.cart'))
        else:
            order = Order(user_id=user_id)
            db.session.add(order)
            order_item = OrderItem(product_id=product.id, user_id=user_id)
            db.session.add(order_item)
            order_item.order = order
            db.session.commit()
            flash('This product was added to your cart', 'success')


    return render_template('product-detail.html', product=product)


@shop_bp.route('/cart')
@login_required
def cart():
    order = Order.query.filter_by(user_id=current_user.id, status=False).first()
    return render_template('cart.html', order=order)



# product_id = request.form.get('product_id')
#     quantity = request.form.get('quantity')

#     if not product_id or not quantity:
#         flash('Missing product ID or quantity', 'error')
#         return redirect(url_for('shop.cart'))

#     try:
#         product_id = int(product_id)
#         quantity = int(quantity)
#     except ValueError:
#         flash('Invalid product ID or quantity', 'error')
#         return redirect(url_for('shop.cart'))

#     product = Product.query.get(product_id)
#     if not product:
#         flash('Product not found', 'error')
#         return redirect(url_for('shop.cart'))

#     order = Order.query.filter_by(user_id=current_user.id).first()
#     if not order:
#         order = Order(user_id=current_user.id)
#         db.session.add(order)

#     order_item = OrderItem.query.filter_by(order_id=order.id, product_id=product_id).first()
#     if order_item:
#         order_item.quantity += quantity
#     else:
#         order_item = OrderItem(order_id=order.id, product_id=product_id, quantity=quantity, subtotal=product.price)
#         db.session.add(order_item)

#     db.session.commit()
#     flash('Product added to cart successfully', 'success')
#     return redirect(url_for('shop.cart'))
