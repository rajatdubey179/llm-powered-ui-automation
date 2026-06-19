from playwright.sync_api import Page


class HotelsPage:
    def __init__(self, page: Page):
        self.page = page
        self.destination_input = page.get_by_role("textbox", name="Destination or Hotel Name")
        self.checkin_input = page.get_by_role("textbox", name="Check-in Date")
        self.checkout_input = page.get_by_role("textbox", name="Check-out Date")
        self.search_button = page.get_by_role("button", name="Search Hotels")
        self.hotel_cards = page.locator(".hotel-item, .property-card, [class*='hotel-card']")
        self.hotel_names = page.locator(".hotel-name, .property-name, h3")

    def open(self):
        self.page.goto("/#stays")
        self.page.wait_for_load_state("networkidle")
        self.page.locator('[role=tab]:has-text("Stays")').click()

    def search(self, destination: str, checkin: str, checkout: str):
        self.destination_input.click()
        self.destination_input.fill(destination)
        self.page.wait_for_timeout(1200)
        self.page.locator(f'li:has-text("{destination}"), .autocomplete-item:has-text("{destination}")').first.click()

        self.checkin_input.click()
        self.checkin_input.fill(checkin)
        self.page.keyboard.press("Escape")

        self.checkout_input.click()
        self.checkout_input.fill(checkout)
        self.page.keyboard.press("Escape")

        self.search_button.click()
        self.page.wait_for_load_state("networkidle")

    def has_results(self) -> bool:
        return self.hotel_cards.count() > 0

    def get_result_count(self) -> int:
        return self.hotel_cards.count()

    def click_first_hotel(self):
        self.hotel_cards.first.click()
        self.page.wait_for_load_state("networkidle")

    def get_hotel_names(self) -> list:
        return [self.hotel_names.nth(i).inner_text() for i in range(min(self.hotel_names.count(), 5))]
