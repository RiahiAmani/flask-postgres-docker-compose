def register(client, username='alice', password='secret123'):
    return client.post('/register', data={'username': username, 'password': password}, follow_redirects=True)

def login(client, username='alice', password='secret123'):
    return client.post('/login', data={'username': username, 'password': password}, follow_redirects=True)
