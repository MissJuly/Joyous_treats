from flask import Blueprint, render_template
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/register')
def register():
    return render_template('register.html')
