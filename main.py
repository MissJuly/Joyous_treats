from flask import Blueprint, render_template


main = Blueprint('main', __name__)


@main.route("/home")
@main.route("/")
def home():
    return render_template('home.html')

@main.route("/shop")
def shop():
    return render_template('shop.html')

@main.route("/shop/cakes")
def cakes():
    return render_template('cakes.html')

@main.route("/shop/pies")
def pies():
    return render_template('pies.html')

@main.route("/shop/pastries")
def pastries():
    return render_template('pastries.html')

@main.route("/shop/fancy-desserts")
def fancy_desserts():
    return render_template('fancy-desserts.html')



if __name__ == "__main__":
    main.run(host='0.0.0.0', debug=True)
