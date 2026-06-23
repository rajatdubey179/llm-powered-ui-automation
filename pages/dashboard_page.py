from playwright.sync_api import Page


class DashboardPage:
    URL = "/dashboard"

    def __init__(self, page: Page):
        self.page = page
        self.user_menu_button = page.get_by_role("button", name="account_circle Demo User expand_more")
        self.my_bookings_link = page.get_by_role("link", name="calendar_month My Bookings")
        self.logout_link = page.get_by_role("banner").get_by_role("link", name="logout Logout")
        self.booking_rows = page.locator("table tbody tr, .booking-item")

    def navigate(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    def is_on_dashboard(self) -> bool:
        return "dashboard" in self.page.url or "/login" not in self.page.url

    def _open_user_menu(self):
        self.user_menu_button.click()
        self.page.wait_for_timeout(500)

    def go_to_my_bookings(self):
        self._open_user_menu()
        self.my_bookings_link.click()
        self.page.wait_for_load_state("networkidle")

    def get_booking_count(self) -> int:
        return self.booking_rows.count()

    def logout(self):
        self._open_user_menu()
        self.logout_link.click()
        self.page.wait_for_load_state("networkidle")
