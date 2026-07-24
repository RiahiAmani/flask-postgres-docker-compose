from tests.helpers import register, login
from app import db, ActiveSessionsCollector
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
        user = User(username='active_user', password='hashed', last_seen=datetime.utcnow())
        db.session.add(user)
        db.session.commit()

        collector = ActiveSessionsCollector()
        metrics = list(collector.collect())
        assert len(metrics) == 1
        assert metrics[0].samples[0].value >= 1

def test_active_sessions_collector_ignores_inactive_users(app):
    with app.app_context():
        old_ts = datetime.utcnow() - timedelta(minutes=10)
        user = User(username='inactive_user', password='hashed', last_seen=old_ts)
        db.session.add(user)
        db.session.commit()

        collector = ActiveSessionsCollector()
        metrics = list(collector.collect())
        value_before = metrics[0].samples[0].value

        active = User(username='fresh_user', password='hashed', last_seen=datetime.utcnow())
        db.session.add(active)
        db.session.commit()

        metrics_after = list(ActiveSessionsCollector().collect())
        value_after = metrics_after[0].samples[0].value
        assert value_after == value_before + 1       
