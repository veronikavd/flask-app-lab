from flask import Blueprint

product_bp = Blueprint('bp', __name__, url_prefix='/')

from . import views