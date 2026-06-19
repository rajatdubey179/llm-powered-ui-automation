from playwright.sync_api import Page


class FlightsPage:
    def __init__(self, page: Page):
        self.page = page
        # trip type buttons
        self.one_way_btn = page.get_by_role("button", name="trending_flat One Way")
        self.round_trip_btn = page.get_by_role("button", name="sync_alt Round Trip")
        # search inputs (inside flights tabpanel)
        self.origin_input = page.get_by_role("textbox", name="Departure From")
        self.destination_input = page.get_by_role("textbox", name="Arrival To")
        self.depart_date_input = page.get_by_role("textbox", name="Departure Date")
        self.search_button = page.get_by_role("button", name="Search Flights")
        self.results = page.locator(".flight-item, .flight-result, [class*='flight-card']")

    def open(self):
        self.page.goto("/#flights")
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("tab", name="flight_takeoff Flights").click()

    def select_one_way(self):
        self.one_way_btn.click()

    def search(self, origin: str, destination: str, date: str):
        self.origin_input.click()
        self.origin_input.fill(origin)
        self.page.wait_for_timeout(1200)
        self.page.locator(f'li:has-text("{origin}"), .autocomplete-item:has-text("{origin}")').first.click()

        self.destination_input.click()
        self.destination_input.fill(destination)
        self.page.wait_for_timeout(1200)
        self.page.locator(f'li:has-text("{destination}"), .autocomplete-item:has-text("{destination}")').first.click()

        self.depart_date_input.click()
        self.depart_date_input.fill(date)
        self.page.keyboard.press("Escape")

        self.search_button.click()
        self.page.wait_for_load_state("networkidle")

    def has_results(self) -> bool:
        return self.results.count() > 0

    def get_result_count(self) -> int:
        return self.results.count()
