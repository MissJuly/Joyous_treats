from flask import Blueprint, render_template


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
    return render_template('cakes.html')

# Define a route for the pies page
@shop_bp.route("/shop/pies")
def pies():
    return render_template('pies.html')

# Define a route for the pastries page
@shop_bp.route("/shop/pastries")
def pastries():
    return render_template('pastries.html')

# Define a route for the fancy desserts page
@shop_bp.route("/shop/fancy-desserts")
def fancy_desserts():
    return render_template('fancy-desserts.html')

# @shop_bp.route("")
# def :
#     return render_template('')
