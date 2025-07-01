
#Login feature for testing new registered user
def login(client, username, password):
    return client.post("/login", data=dict(username=username, password=password), follow_redirects=True)


def test_index_requires_login(client):
    response = client.get("/")
    assert response.status_code == 302  

def test_register_and_login_logout(client):
    response = client.post("/register", data={
        "firstName": "Test",
        "lastName": "User",
        "username": "testuser",
        "password": "testpassword123"
    }, follow_redirects=True)
    assert b"login" in response.data 

    # Login
    response = login(client, "testuser", "testpassword123")
    assert b"Welcome" in response.data 

def test_login_invalid(client):
    response = login(client, "invalidUsername", "invalidPassword")
    print (response.data) 
    assert b"Invalid username or password" in response.data
