import pytest
# from werkzeug.security import generate_password_hash
from databases.models import User, Vendor, Item, ItemCategory
from databases.models.user import AccessRoleEnum
from databases.models.item import StatusEnum
from datetime import date
from databases.createDatabase import hashPassword
import bcrypt


@pytest.fixture
def client():
    from app import create_app
    from databases.base import db
    import os

    test_db = "sqlite:///:memory:"
    app = create_app({
        "SQLALCHEMY_DATABASE_URI": test_db,
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test"
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

        # Add a test admin and user 
        admin = User(firstName="Admin", lastName="User", username="admin", password=hashPassword("adminPassword"), accessRole=AccessRoleEnum.Admin)
        user = User(firstName="Normal", lastName="User", username="normalUser", password=hashPassword("userPassword"), accessRole=AccessRoleEnum.User)
        db.session.add(admin)
        db.session.add(user)
        db.session.commit()

        # Add a vendor
        vendor = Vendor(vendorName="Test Vendor", sustainabilityCertified=True, isDeleted=False)
        db.session.add(vendor)
        db.session.commit()

        # Add an item category
        category = ItemCategory(itemCategoryName="Test Category")
        db.session.add(category)
        db.session.commit()

        # Add an item
        item = Item(vendorID=vendor.vendorID, userID=user.userID, itemCategoryID=category.itemCategoryID, expiryDate=date(2025,6,8), status=StatusEnum.Active, userNotes="Working fine")
        db.session.add(item)
        db.session.commit()
    yield app.test_client()



@pytest.fixture
def login_admin(client):
    client.post("/login", data=dict(username="admin", password="adminPassword"), follow_redirects=True)
    yield
    client.get("/logout", follow_redirects=True)

@pytest.fixture
def login_user(client):
    client.post("/login", data=dict(username="normalUser", password="userPassword"), follow_redirects=True)
    yield

    client.get("/logout", follow_redirects=True)

#asserts standard navbar components
def assert_standard_navbar(response):
    assert b"Home" in response.data 
    assert b"Categories" in response.data
    assert b"Vendors" in response.data 
    assert b"Users" in response.data 
    assert b"Items" in response.data
    assert b"Logout" in response.data

#asserts login navbar components
def assert_login_navigation(response):
    assert b"Login" in response.data
    assert b"Register" in response.data

#asserts footer response
def assert_footer(response):
    assert b"Copyright @ 2025 E-track" in response.data

#asserts common form buttons
def assert_common_form_buttons(response):
    assert b"Cancel" in response.data
    assert b"Return" in response.data
    assert b"btn btn-sm btn-primary" in response.data