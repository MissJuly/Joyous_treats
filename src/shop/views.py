from flask import Blueprint, render_template

shop_bp = Blueprint(
    "shop", __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path="/shop/static"
)

@shop_bp.route("/shop")
def shop():
    return render_template('shop.html')

@shop_bp.route("/shop/cakes")
def cakes():
    return render_template('cakes.html')

@shop_bp.route("/shop/pies")
def pies():
    return render_template('pies.html')

@shop_bp.route("/shop/pastries")
def pastries():
    return render_template('pastries.html')

@shop_bp.route("/shop/fancy-desserts")
def fancy_desserts():
    return render_template('fancy-desserts.html')

# @shop_bp.route("")
# def :
#     return render_template('')
