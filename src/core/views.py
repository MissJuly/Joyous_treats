from flask import Blueprint, render_template


core_bp = Blueprint(
    "core", __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path="/core/static"
)

@core_bp.route("/")
def home():
    return render_template('home.html')


