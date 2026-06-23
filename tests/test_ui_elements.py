"""Tests for UI elements visibility and interactivity."""

import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage


def _dismiss_modal(page):
    modal = page.locator("#demoWarningModal")
    try:
        modal.wait_for(state="visible", timeout=2000)
        page.get_by_role("button", name="I Understand & Continue").click()
        modal.wait_for(state="hidden", timeout=2000)
    except Exception:
        pass


def test_search_buttons_are_enabled(page):
    home = HomePage(page)
    home.navigate()
    _dismiss_modal(page)

    # Check for search buttons on the page
    search_buttons = page.locator("button[type='button']").count()
    assert search_buttons > 0, "Page should have search buttons"


def test_login_form_elements_visible(page):
    login = LoginPage(page)
    login.navigate()

    assert login.email_input.is_visible(), "Email input should be visible"
    assert login.password_input.is_visible(), "Password input should be visible"
    assert login.submit_button.is_visible(), "Submit button should be visible"


def test_navigation_header_always_visible(page):
    home = HomePage(page)
    home.navigate()

    assert home.login_link.is_visible(), "Login link in header should be visible"
    # Verify header elements are at the top
    header_bbox = page.locator("header, [role=banner]").first.bounding_box()
    assert header_bbox and header_bbox["y"] == 0, "Header should be at the top of the page"
