import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


def test_valid_login(page, config):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(config["username"], config["password"])
    dashboard = DashboardPage(page)
    assert dashboard.is_on_dashboard(), "Expected to land on account dashboard after login"


def test_invalid_password(page, config):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(config["username"], "wrongpassword123")
    assert login_page.has_error_message(), "Expected error for wrong password"


def test_invalid_email(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("notauser@fake.com", "somepassword")
    assert login_page.has_error_message(), "Expected error for unregistered email"

#ABC
def test_empty_credentials(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("", "")
    assert login_page.has_error_message() or page.url.__contains__("login"), \
        "Expected to stay on login page with empty credentials"

#Login Page Test case
def test_logout(page, config):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(config["username"], config["password"])
    dashboard = DashboardPage(page)
    assert dashboard.is_on_dashboard()
    dashboard.logout()
    assert "login" in page.url or page.url == page.context.base_url + "/"
