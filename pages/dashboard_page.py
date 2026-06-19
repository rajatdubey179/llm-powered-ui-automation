from playwright.sync_api import Page


class DashboardPage:
    URL = "/account"

    def __init__(self, page: Page):
        self.page = page
        self.my_bookings_link = page.get_by_role("link", name="My Bookings").or_(
            page.locator('a[href*="booking"]')
        ).first
        self.logout_link = page.get_by_role("link", name="Logout").or_(
            page.locator('a[href*="logout"]')
        ).first
        self.booking_rows = page.locator("table tbody tr, .booking-item")

    def navigate(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    def is_on_dashboard(self) -> bool:
        return "/login" not in self.page.url

    def go_to_my_bookings(self):
        self.my_bookings_link.click()
        self.page.wait_for_load_state("networkidle")

    def get_booking_count(self) -> int:
        return self.booking_rows.count()

    def logout(self):
        self.logout_link.click()
        self.page.wait_for_load_state("networkidle")
