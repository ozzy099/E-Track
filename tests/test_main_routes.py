#Testing the main routes blueprint 

#Test an admin can log in to homepage, sees their role, action, and general information 
def test_login_admin(client, login_admin):
    response = client.get("/")
    assert b"Welcome Admin" in response.data 
    assert b"Your role: Admin" in response.data
    assert b"Manage users" in response.data
    assert b"About E-track" in response.data
    assert b"Our Values" in response.data

#Test a normal user can log in to homepage, sees their role, action, and general information
def test_login_user(client, login_user):
    response = client.get("/")
    assert b"Welcome Normal" in response.data 
    assert b"Your role: User" in response.data
    assert b"Manage users" not in response.data
    assert b"About E-track" in response.data
    assert b"Our Values" in response.data

