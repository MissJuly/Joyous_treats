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
def category():
    return render_template('cakes.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
