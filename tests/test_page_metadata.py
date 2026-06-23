"""Tests for page metadata, titles, and SEO elements."""

import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.dashboard_page import DashboardPage


def test_homepage_has_valid_title(page):
    home = HomePage(page)
    home.navigate()
    title = page.title()
    assert title and len(title) > 0, "Homepage should have a valid page title"
    assert "phptravels" in title.lower() or "travel" in title.lower(), \
        "Page title should contain relevant keywords"


def test_login_page_has_descriptive_title(page):
    login = LoginPage(page)
    login.navigate()
    title = page.title()
    assert "login" in title.lower(), "Login page title should contain 'login'"


def test_dashboard_page_accessible_without_errors(page, config):
    login = LoginPage(page)
    login.navigate()
    login.login(config["username"], config["password"])
    dashboard = DashboardPage(page)
    assert dashboard.is_on_dashboard(), "User should be on dashboard after login"
    assert page.url != "", "Dashboard should have a valid URL"
