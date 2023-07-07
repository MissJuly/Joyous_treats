from flask import Blueprint, render_template, jsonify
from src.shop.models import Product



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

# @shop_bp.route("")
# def :
#     return render_template('')

# Api routes
# Retrieve a list of available bakery products
@shop_bp.route('/api/products', methods=['GET'])
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
        product_list.append(product_data)

    return jsonify(product_list)

# Fetch details about a specific product by providing its unique identifier
@shop_bp.route('/api/products/<int:product_id>', methods=['GET'])
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

# Search products in database

