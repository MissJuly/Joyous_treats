from flask import Flask, render_template


app = Flask(__name__)


@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/shop")
def shop():
    return render_template('shop.html')

@app.route("/shop/cakes")
def cakes():
    return render_template('cakes.html')

@app.route("/shop/pies")
def pies():
    return render_template('pies.html')

@app.route("/shop/pastries")
def pastries():
    return render_template('pastries.html')

@app.route("/shop/fancy-desserts")
def fancy_desserts():
    return render_template('fancy-desserts.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
