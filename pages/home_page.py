from playwright.sync_api import Page


class HomePage:
    URL = "/"

    def __init__(self, page: Page):
        self.page = page
        self.flights_tab = page.get_by_role("tab", name="flight_takeoff Flights")
        self.stays_tab = page.get_by_role("tab", name="hotel Stays")
        self.tours_tab = page.get_by_role("tab", name="explore Tours")
        self.cars_tab = page.get_by_role("tab", name="directions_car Cars")
        self.login_link = page.get_by_role("link", name="login Login")

    def navigate(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    def open_flights_tab(self):
        self.flights_tab.click()

    def open_stays_tab(self):
        self.stays_tab.click()

    def open_tours_tab(self):
        self.tours_tab.click()

    def go_to_login(self):
        self.login_link.click()
        self.page.wait_for_load_state("networkidle")
