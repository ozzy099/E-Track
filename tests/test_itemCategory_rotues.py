# Testing for the item category routes

import databases.models as models
from databases.base import db
import pytest

#test admin can delete an item category and sees the Deleted Item Categories table
def test_admin_deletes_item_category(client, login_admin):
    with client.application.app_context():
        item_category = db.session.get(models.ItemCategory, 1)
        assert item_category.isDeleted is False
    response = client.get("/categories/delete/1", follow_redirects=True)
    assert b"Item category deleted successfully!" in response.data
    assert b"Deleted Item Categories" in response.data
    assert b"Restore" in response.data
    with client.application.app_context():
        item_category = db.session.get(models.ItemCategory, 1)
        assert item_category.isDeleted is True

#test user cannot delete an item category and sees danger alert
def test_user_cannot_delete_item_category(client, login_user):
    response = client.get("/categories/delete/1", follow_redirects=True)
    assert b"Access denied! You do not have permission to delete item categories" in response.data
    with client.application.app_context():
        item_category = db.session.get(models.ItemCategory, 1)
        assert item_category.isDeleted is False

#test admin can restore a deleted item category and  alert appears
def test_admin_restores_deleted_item_category(client, login_admin):
    with client.application.app_context():
        models.ItemCategory.query.update({models.ItemCategory.isDeleted: True})
        db.session.commit()
        itemCategory = models.ItemCategory.query.filter_by(isDeleted=True).first()
        response = client.get(f"/categories/restore/{itemCategory.itemCategoryID}", follow_redirects=True)
        assert b"Item category restored successfully!" in response.data
        restoredItemCategory = db.session.get(models.ItemCategory, itemCategory.itemCategoryID)
        assert restoredItemCategory.isDeleted is False
        assert b"Attention! There are no deleted records" in response.data

#test user cannot restore an item category and sees danger alert
def test_user_cannot_restore_item_category(client, login_user):
    with client.application.app_context():
        models.ItemCategory.query.update({models.ItemCategory.isDeleted: True})
        db.session.commit()
    response = client.get("/categories/restore/1", follow_redirects=True)
    assert b"Access denied! You do not have permission to restore item categories" in response.data
    with client.application.app_context():
        item_category = db.session.get(models.ItemCategory, 1)
        assert item_category.isDeleted is True

#test user does not see the deleted item categories heading, the none deleted alert, and the delete button
def test_user_does_not_see_deleted_item_categories(client, login_user):
    response = client.get("/categories")
    assert b"Deleted Item Categories" not in response.data
    assert b'btn btn-sm btn-danger' not in response.data
    assert b"Attention! There are no deleted records" not in response.data

#test user sees active item categories and the edit button
def test_user_sees_active_item_categories(client, login_user):
    response = client.get("/categories")
    assert b"Active Item Categories" in response.data
    assert b"Test Category" in response.data
    assert b"edit" in response.data

#defining array to be used for paramterized tests
categoryCreateFormRoutes = ["/categories/create", "/categories/update/1"]

#testing the create category form field renders correctly
@pytest.mark.parametrize("category_form_routes", categoryCreateFormRoutes)
def test_category_form_fields_render(client, login_user, category_form_routes):
    response = client.get(category_form_routes, follow_redirects=True)
    assert b"Enter item category" in response.data


#test item category invalid form returns error message
@pytest.mark.parametrize("category_form_routes", categoryCreateFormRoutes)
def test_category_form_invalid_submission(client, login_user, category_form_routes):
    response = client.post(category_form_routes, data={
        "itemCategoryName": "",
    }, follow_redirects=True)
    assert b"Enter item category" in response.data
    assert b"This field is required" in response.data

#test the create item category form updates the database and the Active Item Categories table
def test_create_form_updates (client, login_user):
    response = client.post("/categories/create", data={
        "itemCategoryName": "Created Category"
    }, follow_redirects=True)
    assert b"Item category created successfully!" in response.data

    response = client.get("/categories")
    assert b"Active Item Categories" in response.data
    assert b"Created Category" in response.data

