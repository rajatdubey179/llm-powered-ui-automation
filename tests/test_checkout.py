import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@pytest.fixture(autouse=True)
def login(page, config):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(config["username"], config["password"])
    assert DashboardPage(page).is_on_dashboard(), "Login failed before checkout test"


def test_dashboard_loads_after_login(page):
    dashboard = DashboardPage(page)
    dashboard.navigate()
    assert dashboard.is_on_dashboard()


def test_my_bookings_accessible(page):
    dashboard = DashboardPage(page)
    dashboard.navigate()
    dashboard.go_to_my_bookings()
    assert "booking" in page.url.lower(), "Expected to navigate to bookings page"


def test_booking_list_visible(page):
    dashboard = DashboardPage(page)
    dashboard.navigate()
    dashboard.go_to_my_bookings()
    count = dashboard.get_booking_count()
    assert count >= 0, "Booking count should be a non-negative number"
