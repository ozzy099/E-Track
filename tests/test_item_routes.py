# Testing for the item routes
import databases.models as models
from databases.base import db
import pytest


#test admin can delete an item and sees the Deleted Items table
def test_admin_deletes_item(client, login_admin):
    with client.application.app_context():
        item = db.session.get(models.Item, 1)
        assert item.isDeleted is False
    response = client.get("/items/delete/1", follow_redirects=True)
    assert b"Item deleted successfully!" in response.data
    assert b"Deleted Items" in response.data
    assert b"Restore" in response.data
    with client.application.app_context():
        item = db.session.get(models.Item, 1)
        assert item.isDeleted is True

#test user cannot delete an item and sees danger alert
def test_user_cannot_delete_item(client, login_user):
    response = client.get("/items/delete/1", follow_redirects=True)
    assert b"Access denied! You do not have permission to delete items" in response.data
    with client.application.app_context():
        item = db.session.get(models.Item, 1)
        assert item.isDeleted is False

#test admin can restore a deleted item and the alert reappears
def test_admin_restores_deleted_item(client, login_admin):
    with client.application.app_context():
        models.Item.query.update({models.Item.isDeleted: True})
        db.session.commit()
        item = models.Item.query.filter_by(isDeleted=True).first()
        response = client.get(f"/items/restore/{item.itemID}", follow_redirects=True)
        assert b"Item restored successfully!" in response.data
        restoredItem = db.session.get(models.Item, item.itemID)
        assert restoredItem.isDeleted is False
        assert b"Attention! There are no deleted records" in response.data

#test user cannot restore an item and sees danger alert
def test_user_cannot_restore_item(client, login_user):
    with client.application.app_context():
        models.Item.query.update({models.Item.isDeleted: True})
        db.session.commit()
    response = client.get("/items/restore/1", follow_redirects=True)
    assert b"Access denied! You do not have permission to restore items" in response.data
    with client.application.app_context():
        item = db.session.get(models.Item, 1)
        assert item.isDeleted is True

#test user does not see the deleted items heading, the none deleted alert, and the delete button: 
def test_user_does_not_see_admin_only_attributes(client, login_user):
    response = client.get("/items")
    assert b"Deleted Items" not in response.data
    assert b'btn btn-sm btn-danger' not in response.data
    assert b"Attention! There are no deleted records" not in response.data

#test user sees active items and the edit button
def test_user_sees_active_items(client, login_user):
    response = client.get("/items")
    assert b"Active Items" in response.data
    assert b"Working fine" in response.data
    assert b"edit" in response.data

#defining array to be used for paramterized tests 
itemCreateFormRoutes = ["/items/create", "/items/update/1"]

#testing the create item form fields render correctly 
@pytest.mark.parametrize("item_form_routes", itemCreateFormRoutes)
def test_item_form_fields_render(client, login_user, item_form_routes):
    response = client.get(item_form_routes, follow_redirects=True)
    assert b"Vendor" in response.data
    assert b"User" in response.data
    assert b"Item Category" in response.data
    assert b"Expiry Date" in response.data
    assert b"Status" in response.data
    assert b"Optional User Notes" in response.data

#test the create item form updates the database and the Active Items table
def test_create_form_updates (client, login_user):
    response = client.post("/items/create", data={
       "vendorID": "1",
        "userID": "1",
        "itemCategoryID": "1",
        "expiryDate": "2025-12-31",
        "status": "Active",
        "userNotes": "Test notes"
    }, follow_redirects=True)
    assert b"Item created successfully!" in response.data

    response = client.get("/items")
    assert b"Active Items" in response.data
    assert b"Test notes" in response.data


