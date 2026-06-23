"""Tests for homepage visibility and feature presence."""

import pytest
from pages.home_page import HomePage


def test_homepage_loads_successfully(page):
    home = HomePage(page)
    home.navigate()
    assert page.url.endswith("/"), "Expected homepage URL"
    assert page.title() != "", "Expected page title to be present"


def test_all_main_tabs_visible(page):
    home = HomePage(page)
    home.navigate()
    assert home.flights_tab.is_visible(), "Flights tab should be visible"
    assert home.stays_tab.is_visible(), "Stays tab should be visible"
    assert home.tours_tab.is_visible(), "Tours tab should be visible"
    assert home.cars_tab.is_visible(), "Cars tab should be visible"


def test_login_link_accessible_on_homepage(page):
    home = HomePage(page)
    home.navigate()
    assert home.login_link.is_visible(), "Login link should be visible on homepage"
    login_url = home.login_link.get_attribute("href")
    assert login_url and "login" in login_url.lower(), "Login link should point to login page"
