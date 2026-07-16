from tests.helpers import register, login
from app.models import Task

def test_index_requires_login(client):
    response = client.get('/', follow_redirects=True)
    assert b'Login' in response.data

def test_add_task(client):
    register(client, 'bob', 'pass1234')
    login(client, 'bob', 'pass1234')
    response = client.post('/add', data={'title': 'Buy milk'}, follow_redirects=True)
    assert b'Buy milk' in response.data

def test_complete_task_toggle(client, app):
    register(client, 'bob', 'pass1234')
    login(client, 'bob', 'pass1234')
    client.post('/add', data={'title': 'Wash car'}, follow_redirects=True)
    with app.app_context():
        task = Task.query.filter_by(title='Wash car').first()
    response = client.get(f'/complete/{task.id}', follow_redirects=True)
    assert response.status_code == 200

def test_delete_task(client, app):
    register(client, 'bob', 'pass1234')
    login(client, 'bob', 'pass1234')
    client.post('/add', data={'title': 'Temp task'}, follow_redirects=True)
    with app.app_context():
        task = Task.query.filter_by(title='Temp task').first()
    response = client.get(f'/delete/{task.id}', follow_redirects=True)
    assert b'Temp task' not in response.data

def test_cannot_modify_others_task(client, app):
    register(client, 'carol', 'pw12345')
    login(client, 'carol', 'pw12345')
    client.post('/add', data={'title': 'Carol task'}, follow_redirects=True)
    with app.app_context():
        task = Task.query.filter_by(title='Carol task').first()
    client.get('/logout', follow_redirects=True)

    register(client, 'dave', 'pw67890')
    login(client, 'dave', 'pw67890')
    response = client.get(f'/delete/{task.id}', follow_redirects=True)
    assert b'Carol task' in response.data
