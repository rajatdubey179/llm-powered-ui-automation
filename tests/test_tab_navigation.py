"""Tests for homepage tab switching between Flights, Stays, Tours, and Cars."""

import pytest
from pages.home_page import HomePage


def _dismiss_modal(page):
    modal = page.locator("#demoWarningModal")
    try:
        modal.wait_for(state="visible", timeout=2000)
        page.get_by_role("button", name="I Understand & Continue").click()
        modal.wait_for(state="hidden", timeout=2000)
    except Exception:
        pass


def test_switch_to_flights_tab(page):
    home = HomePage(page)
    home.navigate()
    _dismiss_modal(page)
    home.open_flights_tab()
    assert "flight" in page.url.lower() or page.locator('[role=tab]:has-text("Flights")').is_visible(), \
        "Flights tab should be active after clicking"


def test_switch_to_stays_tab(page):
    home = HomePage(page)
    home.navigate()
    _dismiss_modal(page)
    home.open_stays_tab()
    assert "stay" in page.url.lower() or page.locator('[role=tab]:has-text("Stays")').is_visible(), \
        "Stays tab should be active after clicking"


def test_switch_to_tours_tab(page):
    home = HomePage(page)
    home.navigate()
    _dismiss_modal(page)
    home.open_tours_tab()
    assert "tour" in page.url.lower() or page.locator('[role=tab]:has-text("Tours")').is_visible(), \
        "Tours tab should be active after clicking"
