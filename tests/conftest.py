import pytest
from app import create_app, db as _db

@pytest.fixture
def app():
    test_config = {
        'SECRET_KEY': 'test-secret-key-not-for-production',
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
    }
    flask_app = create_app(test_config)
    yield flask_app
    with flask_app.app_context():
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
