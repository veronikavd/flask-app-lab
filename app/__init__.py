from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key_lab4'  # <--- ДОДАЙТЕ ЦЕЙ РЯДОК

from app import views
from app.users import user_bp
app.register_blueprint(user_bp, url_prefix="/users")

from app.products import product_bp
app.register_blueprint(product_bp, url_prefix="/products")