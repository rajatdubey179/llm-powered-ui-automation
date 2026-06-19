import pytest
from pages.hotels_page import HotelsPage


def test_hotels_page_loads(page):
    hotels = HotelsPage(page)
    hotels.navigate()
    assert "hotel" in page.url.lower() or page.title() != ""


def test_search_hotels_returns_results(page):
    hotels = HotelsPage(page)
    hotels.navigate()
    hotels.search_hotels(city="Dubai", checkin="2025-09-20", checkout="2025-09-25")
    assert hotels.has_results(), "Expected hotel listings after search"


def test_search_results_have_names(page):
    hotels = HotelsPage(page)
    hotels.navigate()
    hotels.search_hotels(city="Dubai", checkin="2025-09-20", checkout="2025-09-25")
    names = hotels.get_hotel_names()
    assert len(names) > 0, "Expected hotel names to be displayed"
    assert all(len(name.strip()) > 0 for name in names), "Hotel names should not be empty"


def test_click_hotel_opens_detail(page):
    hotels = HotelsPage(page)
    hotels.navigate()
    hotels.search_hotels(city="Dubai", checkin="2025-09-20", checkout="2025-09-25")
    assert hotels.has_results()
    hotels.click_first_hotel()
    assert "hotel" in page.url.lower(), "Expected to navigate to hotel detail page"
