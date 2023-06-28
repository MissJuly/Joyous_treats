from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import mysql.connector
import os


load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@<hostname>/{}'.format(os.environ.get("username"), os.environ.get("password"), os.environ.get("database"))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'thisisasecretkey'

    db.init_app(app)

    # blueprint for authentication routes in app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-authentication parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
