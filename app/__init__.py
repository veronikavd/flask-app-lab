from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.views import main_bp
    app.register_blueprint(main_bp)

    from app.users import user_bp
    app.register_blueprint(user_bp, url_prefix="/users")

    from app.products import product_bp
    app.register_blueprint(product_bp, url_prefix="/products")

    from app.posts import post_bp
    app.register_blueprint(post_bp, url_prefix="/post")

    return app