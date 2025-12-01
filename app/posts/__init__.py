from flask import Blueprint

post_bp = Blueprint('posts', __name__, template_folder='templates')

from . import views