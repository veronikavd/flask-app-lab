import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'a_super_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'app.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager.init_app(app) 
    login_manager.login_view = 'bp.login'
    login_manager.login_message_category = 'info'
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    
    with app.app_context():
        from . import models
        from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    from app.products import product_bp 
    app.register_blueprint(product_bp) 

    return app