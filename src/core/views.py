from flask import Blueprint, render_template

# Create a Blueprint for core module
core_bp = Blueprint(
    "core", __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path="/core/static"
)

# Define the home route and render the template
@core_bp.route("/")
def home():
    return render_template('home.html')

