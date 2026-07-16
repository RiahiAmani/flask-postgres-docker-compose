from app import db
from app.models import User, Task
from werkzeug.security import generate_password_hash

def test_create_user_and_task(app):
    with app.app_context():
        user = User(username='eve', password=generate_password_hash('pw'))
        db.session.add(user)
        db.session.commit()

        task = Task(title='Test task', owner=user)
        db.session.add(task)
        db.session.commit()

        assert task.id is not None
        assert task.completed is False
        assert task.owner.username == 'eve'
