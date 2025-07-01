# Testing for the user routes

import databases.models as models
from databases.base import db
import pytest


#test admin can delete a user and sees the Deleted Users table
def test_admin_deletes_user(client, login_admin):
    with client.application.app_context():
        user = db.session.get(models.User, 2)
        assert user.isDeleted is False
    response = client.get("/users/delete/2", follow_redirects=True)
    assert b"User deleted successfully!" in response.data
    assert b"Deleted Users" in response.data
    assert b"Restore" in response.data
    with client.application.app_context():
        user = db.session.get(models.User, 2)
        assert user.isDeleted is True

#test admin can restore a deleted user and the alert reappears
def test_admin_restores_deleted_user(client, login_admin):
    with client.application.app_context():
        user = db.session.get(models.User, 2)
        user.isDeleted = True
        db.session.commit()
        user = models.User.query.filter_by(isDeleted=True).first()
        response = client.get(f"/users/restore/{user.userID}", follow_redirects=True)
        assert b"User restored successfully!" in response.data
        restoredUser = db.session.get(models.User, user.userID)
        assert restoredUser.isDeleted is False
        assert b"Attention! There are no deleted records" in response.data

#test user cannot delete a user and sees danger alert
def test_user_cannot_delete_user(client, login_user):
    response = client.get("/users/delete/2", follow_redirects=True)
    assert b"Access denied! You do not have permission to delete users" in response.data
    with client.application.app_context():
        user = db.session.get(models.User, 2)
        assert user.isDeleted is False

#defining array to be used for parameterized tests
userCreateFormRoutes = ["/users/create", "/users/update/2"]


#testing the create user form fields render correctly 
@pytest.mark.parametrize("user_form_routes", userCreateFormRoutes)
def test_user_form_fields_render(client, login_admin, user_form_routes):
    response = client.get(user_form_routes)
    assert b"First Name" in response.data or b"Update User" in response.data
    assert b"Last Name" in response.data
    assert b"Username" in response.data
    assert b"Password" in response.data
    assert b"Access Role" in response.data

#test user invalid form returns error message
@pytest.mark.parametrize("user_form_routes", userCreateFormRoutes)
def test_user_form_invalid_submission(client, login_admin, user_form_routes):
    response = client.post(user_form_routes, data={
        "firstName": "",
        "lastName": "",
        "username": "",
        "password": "",
        "accessRole": ""
    }, follow_redirects=True)
    assert b"This field is required" in response.data


#test the create user form updates the database and the Active Users table
def test_create_form_updates (client, login_admin):
    response = client.post("/users/create", data={
        "firstName": "CreatedUser",
        "lastName": "LastName",
        "username": "createduser67",
        "password": "password123",
        "accessRole": "User"
    }, follow_redirects=True)
    print(response.data.decode())
    assert b"User added successfully!" in response.data

    response = client.get("/users")
    assert b"Active Users" in response.data
    assert b"CreatedUser" in response.data



#test user cannot restore a user and sees danger alert
def test_user_cannot_restore_user(client, login_user):
    with client.application.app_context():
        user = db.session.get(models.User, 1)
        user.isDeleted = True
        db.session.commit()
    response = client.get("/users/restore/1", follow_redirects=True)
    assert b" Access denied! You do not have permission to restore users" in response.data
    with client.application.app_context():
        user = db.session.get(models.User, 1)
        assert user.isDeleted is True

#test user does not see the any users features and only the alert
def test_user_does_not_see_admin_only_attributes(client, login_user):
    response = client.get("/users")
    assert b"Warning!" in response.data
    assert b"You do not have permission to manage user records" in response.data
    assert b"Active Users" not in response.data
    assert b"Deleted Users" not in response.data
    assert b'btn btn-sm btn-danger' not in response.data
    assert b"Attention! There are no deleted records" not in response.data
