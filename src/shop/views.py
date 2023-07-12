from flask import Blueprint, render_template, jsonify, request, session
from sqlalchemy import or_
from src import db
from src.shop.models import Product, Order, OrderItem
from src.shop.forms import ProductForm, SearchForm



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

@shop_bp.route('/product-detail/<int:product_id>',  methods=['GET', 'POST'])
def product_detail(product_id):
    product = Product.query.get(product_id)
    return render_template('product-detail.html', product=product)


@shop_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity')

    if not product_id or not quantity:
        return jsonify({'message': 'Invalid product ID or quantity'})

    try:
        product_id = int(product_id)
        quantity = int(quantity)
    except ValueError:
        return jsonify({'message': 'Invalid product ID or quantity'})

    product = Product.query.get(product_id)  # Assuming you have a way to retrieve products from the database

    if not product:
        return jsonify({'message': 'Product not found'})

    if 'cart' not in session:
        session['cart'] = []

    cart_item = {'product': product, 'quantity': quantity}
    session['cart'].append(cart_item)

    return jsonify({'message': 'Product added to cart successfully!', 'cart_item': cart_item})


@shop_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    """Remove a product from the cart"""
    product_id = int(request.form['product_id'])

    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['product'].id != product_id]

    return jsonify({'message': 'Product removed from cart successfully!'})


@shop_bp.route('/update_quantity', methods=['POST'])
def update_quantity():
    """Update the quantity of a product in the cart"""
    product_id = int(request.form['product_id'])
    quantity = int(request.form['quantity'])

    if 'cart' in session:
        for item in session['cart']:
            if item['product'].id == product_id:
                item['quantity'] = quantity
                break

    return jsonify({'message': 'Quantity updated successfully!'})


@shop_bp.route('/clear_cart')
def clear_cart():
    """Clear all items from the cart"""
    if 'cart' in session:
        session.pop('cart', None)

    return jsonify({'message': 'Cart cleared successfully!'})


@shop_bp.route('/cart')
def cart():
    """Render the cart modal"""
    cart_items = session.get('cart', [])
    total_amount = calculate_total_amount(cart_items)

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)


def calculate_total_amount(cart_items):
    """Calculate the total amount of the items in the cart"""
    total_amount = 0.0
    for item in cart_items:
        total_amount += item['product'].price * item['quantity']
    return total_amount
