from tests.helpers import register, login

def test_register_creates_user(client):
    response = register(client, 'alice', 'secret123')
    assert response.status_code == 200
    assert b'please login' in response.data

def test_register_duplicate_username(client):
    register(client, 'alice', 'secret123')
    response = register(client, 'alice', 'secret123')
    assert b'already exists' in response.data

def test_login_success(client):
    register(client, 'alice', 'secret123')
    response = login(client, 'alice', 'secret123')
    assert b'My Tasks' in response.data

def test_login_invalid_password(client):
    register(client, 'alice', 'secret123')
    response = login(client, 'alice', 'wrongpass')
    assert b'Invalid username or password' in response.data

def test_logout(client):
    register(client, 'alice', 'secret123')
    login(client, 'alice', 'secret123')
    response = client.get('/logout', follow_redirects=True)
    assert b'Login' in response.data
