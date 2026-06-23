"""Tests for user navigation and menu interactions."""

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@pytest.fixture(autouse=True)
def login(page, config):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(config["username"], config["password"])


def test_user_menu_opens_on_click(page):
    dashboard = DashboardPage(page)
    dashboard.navigate()
    dashboard.user_menu_button.click()
    page.wait_for_timeout(500)
    assert dashboard.my_bookings_link.is_visible(), "My Bookings should be visible after menu opens"


def test_navigate_to_dashboard_from_any_page(page, config):
    dashboard = DashboardPage(page)
    page.goto(config["base_url"])
    dashboard.navigate()
    assert dashboard.is_on_dashboard(), "Should successfully navigate to dashboard"


def test_user_menu_has_profile_option(page):
    dashboard = DashboardPage(page)
    dashboard.navigate()
    dashboard.user_menu_button.click()
    page.wait_for_timeout(500)
    profile_link = page.get_by_role("link", name="person Profile").first
    assert profile_link.is_visible(), "Profile link should be visible in user menu"
