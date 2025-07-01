# Testing for the vendor routes

import databases.models as models
from databases.base import db
import pytest

#test admin can delete a vendor and sees the Deleted Vendors table
def test_admin_deletes_vendor(client, login_admin):
    with client.application.app_context():
        vendor = db.session.get(models.Vendor, 1)
        assert vendor.isDeleted is False
    response = client.get("/vendors/delete/1", follow_redirects=True)
    assert b"Vendor deleted successfully!" in response.data
    assert b"Deleted Vendors" in response.data 
    assert b"Restore" in response.data 
    with client.application.app_context():
        vendor = db.session.get(models.Vendor, 1)
        assert vendor.isDeleted is True

#test user cannot delete a vendor and sees danger alert
def test_user_cannot_delete_vendor(client, login_user):
    response = client.get("/vendors/delete/1", follow_redirects=True)
    assert b"Access denied! You do not have permission to delete vendors" in response.data
    with client.application.app_context():
        vendor = db.session.get(models.Vendor, 1)
        assert vendor.isDeleted is False  

#test admin can restore a deleted vendor and the alert reappears 
def test_admin_restores_deleted_vendor(client, login_admin):
    with client.application.app_context():
        models.Vendor.query.update({models.Vendor.isDeleted: True})
        db.session.commit()
        vendor = models.Vendor.query.filter_by(isDeleted=True).first()
        response = client.get(f"/vendors/restore/{vendor.vendorID}", follow_redirects=True)
        assert b"Vendor restored successfully!" in response.data 
        restoredVendor = db.session.get(models.Vendor, vendor.vendorID)
        assert restoredVendor.isDeleted is False
        assert b"Attention! There are no deleted records" in response.data 


#test user cannot restore a vendor and sees danger alert
def test_user_cannot_restore_vendor(client, login_user):
    with client.application.app_context():
        models.Vendor.query.update({models.Vendor.isDeleted: True})
        db.session.commit()
    response = client.get("/vendors/restore/1", follow_redirects=True)
    assert b"Access denied! You do not have permission to restore vendors" in response.data
    with client.application.app_context():
        vendor = db.session.get(models.Vendor, 1)
        assert vendor.isDeleted is True
    

#test user does not see the deleted vendors heading, the none deleted alert, and the delete button: 
def test_user_does_not_see_admin_only_attributes(client, login_user):
    response = client.get("/vendors")
    assert b"Deleted Vendors" not in response.data
    assert b'btn btn-sm btn-danger' not in response.data
    assert b"Attention! There are no deleted records" not in response.data

#test user sees active vendors and the edit button
def test_user_sees_active_vendors(client, login_user):
    response = client.get("/vendors")
    assert b"Active Vendors" in response.data
    assert b"Test Vendor" in response.data 
    assert b"edit" in response.data


#defining array to be used for paramterized tests 
vendorCreateFormRoutes = ["/vendors/create", "/vendors/update/1"]

#testing the create vendor form fields render correctly 
@pytest.mark.parametrize("vendor_form_routes", vendorCreateFormRoutes)
def test_vendor_form_fields_render(client, login_user, vendor_form_routes):
    response = client.get(vendor_form_routes, follow_redirects=True)
    assert b"Vendor Name" in response.data
    assert b"Sustainability Certified" in response.data


#test vendor invalid form returns error message
@pytest.mark.parametrize("vendor_form_routes", vendorCreateFormRoutes)
def test_vendor_form_invalid_submission(client, login_user, vendor_form_routes):
    response = client.post(vendor_form_routes, data={
        "vendorName": "",  
        "sustainabilityCertified": True
    }, follow_redirects=True)
    assert b"Vendor Name" in response.data  
    assert b"This field is required" in response.data

#test the create vendor form updates the database and the Active Vendors table
def test_create_form_updates (client, login_user):
    response = client.post("/vendors/create", data={
        "vendorName": "Created Vendor",
        "sustainabilityCertified": True
    }, follow_redirects=True)
    assert b"Vendor added successfully!" in response.data

    response = client.get("/vendors")
    assert b"Active Vendors" in response.data
    assert b"Created Vendor" in response.data



