#testing common components of the application

import pytest
from tests.conftest import assert_footer, assert_login_navigation, assert_standard_navbar, assert_common_form_buttons

@pytest.mark.parametrize("logged_in_routes", [
    "/",
    "/vendors",
    "/vendors/create",
    "/vendors/update/1", 
    "/vendors/delete/1",
    "/vendors/restore/1", 
    "/categories",
    "/categories/create",
    "/categories/update/1",
    "/categories/delete/1",
    "/categories/restore/1",
    "/items",
    "/items/create",
    "/items/update/1",
    "/items/delete/1",
    "/items/restore/1",
    "/users",
    "/users/create",
    "/users/update/1",
    "/users/restore/1"
])
#test all routes protected by login_required decorator shows the standard navbar and footer
def test_logged_in_components(client, login_admin, logged_in_routes):
    response = client.get(logged_in_routes, follow_redirects=True)
    assert_standard_navbar(response)
    assert_footer(response)


@pytest.mark.parametrize("logged_out_routes", [
    "/login",
    "/register"
])

#test the login and register routes show the footer and login navbar
def test_logged_out_components(client, login_admin, logged_out_routes):
    response = client.get(logged_out_routes, follow_redirects=True)
    assert_login_navigation(response)
    assert_footer(response)


@pytest.mark.parametrize("form_routes",[
    "/vendors/create",
    "/vendors/update/1",
    "/categories/create",
    "/categories/update/1",
    "/items/create",
    "/items/update/1",
    "/users/create",
    "/users/update/1"
])
#testing common form components: buttons
def test_form_components(client, login_admin, form_routes):
    response = client.get(form_routes, follow_redirects=True)
    assert_common_form_buttons(response)


@pytest.mark.parametrize("list_routes", [
    "/vendors",
    "/categories",
    "/items",
    "/users"
])
#test admin can see the alert when there are no deleted records
def test_admin_sees_none_deleted_alert(client, login_admin, list_routes):
    response = client.get(list_routes)
    assert b"Attention! There are no deleted records" in response.data 