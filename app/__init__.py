from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_wtf import CSRFProtect
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from datetime import datetime, timedelta
import os

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

class ActiveSessionsCollector:
    def collect(self):
        from app.models import User
        threshold = datetime.utcnow() - timedelta(minutes=5)
        count = User.query.filter(User.last_seen >= threshold).count()
        gauge = GaugeMetricFamily(
            'taskmanager_active_sessions',
            "Nombre d'utilisateurs actifs au cours des 5 dernières minutes"
        )
        gauge.add_metric([], count)
        yield gauge

def create_app(test_config=None):
    app = Flask(__name__)
    metrics = PrometheusMetrics(app)
    metrics.info('taskmanager_app_info', 'Task Manager application info', version='1.0')
    REGISTRY.register(ActiveSessionsCollector())

    if test_config is None:
        secret_key = os.getenv('SECRET_KEY')
        if not secret_key:
            raise RuntimeError("SECRET_KEY environment variable must be set")
        app.config['SECRET_KEY'] = secret_key
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DATABASE_USER','user')}:{os.getenv('DATABASE_PASSWORD','password')}@{os.getenv('DATABASE_HOST','db')}/{os.getenv('DATABASE_NAME','mydb')}"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    else:
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.auth import auth as auth_blueprint
    from app.routes import main as main_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    @app.before_request
    def update_last_seen():
        if current_user.is_authenticated:
            now = datetime.utcnow()
            if not current_user.last_seen or (now - current_user.last_seen) > timedelta(minutes=1):
                current_user.last_seen = now
                db.session.commit()

    with app.app_context():
        db.create_all()
    return app
