from playwright.sync_api import Page


class LoginPage:
    URL = "/login"

    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.get_by_role("textbox", name="Email Address")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.submit_button = page.get_by_role("button", name="Sign In to your account")
        self.error_alert = page.locator(".alert-danger, .error-message, [class*='error']").first

    def navigate(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")
        modal = self.page.locator("#demoWarningModal")
        if modal.is_visible():
            self.page.get_by_role("button", name="I Understand & Continue").click()
            modal.wait_for(state="hidden")

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()
        self.page.wait_for_load_state("networkidle")

    def is_logged_in(self) -> bool:
        return "/login" not in self.page.url

    def has_error_message(self) -> bool:
        return self.error_alert.is_visible()

    def get_error_text(self) -> str:
        return self.error_alert.inner_text()
