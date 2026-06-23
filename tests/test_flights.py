import pytest
from pages.flights_page import FlightsPage


def test_flights_page_loads(page):
    flights = FlightsPage(page)
    flights.open()
    assert "flight" in page.url.lower() or page.title() != ""


def test_search_one_way_flight(page):
    flights = FlightsPage(page)
    flights.open()
    flights.select_one_way()
    flights.search(origin="Dubai", destination="London", date="2025-09-15")
    assert flights.has_results(), "Expected flight results after search"


def test_search_returns_multiple_results(page):
    flights = FlightsPage(page)
    flights.open()
    flights.search(origin="Dubai", destination="London", date="2025-09-15")
    assert flights.get_result_count() > 1, "Expected more than one flight result"
