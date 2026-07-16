from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
import os

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        raise RuntimeError("SECRET_KEY environment variable must be set")
    app.config['SECRET_KEY'] = secret_key

    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DATABASE_USER','user')}:{os.getenv('DATABASE_PASSWORD','password')}@{os.getenv('DATABASE_HOST','db')}/{os.getenv('DATABASE_NAME','mydb')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.auth import auth as auth_blueprint
    from app.routes import main as main_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()
    return app
