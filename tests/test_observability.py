from tests.helpers import register, login
from app import db
from app.models import User
from datetime import datetime, timedelta

def test_last_seen_updated_on_request(client, app):
    register(client, 'frank', 'pass1234')
    login(client, 'frank', 'pass1234')

    with app.app_context():
        user = User.query.filter_by(username='frank').first()
        assert user.last_seen is not None

def test_active_sessions_collector_counts_recent_users(app):
    with app.app_context():
        user = User.query.filter_by(username='frank').first()
        if user is None:
            user = User(username='frank2', password='hashed')
            db.session.add(user)
        user.last_seen = datetime.utcnow()
        db.session.commit()

        from app import ActiveSessionsCollector
        collector = ActiveSessionsCollector()
        metrics = list(collector.collect())
        assert len(metrics) == 1
        assert metrics[0].samples[0].value >= 1

def test_active_sessions_collector_ignores_old_users(app):
    with app.app_context():
        user = User(username='old_user', password='hashed', last_seen=datetime.utcnow() - timedelta(minutes=10))
        db.session.add(user)
        db.session.commit()

        from app import ActiveSessionsCollector
        collector = ActiveSessionsCollector()
        metrics = list(collector.collect())
       
