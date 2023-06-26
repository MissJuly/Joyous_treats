from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin


app = Flask(__name__)
# db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SECRET_KEY'] = 'thisisasecretkey'


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
