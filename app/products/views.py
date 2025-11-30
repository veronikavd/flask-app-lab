from flask import render_template
from . import product_bp

@product_bp.route("/")
def index():
    return render_template("products/index.html")