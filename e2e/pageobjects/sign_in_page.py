"""SignInPage handles login functionality."""

from playwright.sync_api import Page, Locator
from e2e.common.base_page import BasePage


class SignInPage(BasePage):
    """Page object for the sign-in page."""
    
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input: Locator = page.locator('#username')
        self.password_input: Locator = page.locator('#password')
    
    def goto(self) -> None:
        """Navigate to the sign-in page."""
        self.navigate_to("/signin")
    
    def login(self, username: str, password: str) -> None:
        """Login with the provided username and password."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.click_button("Sign In")
        self.page.wait_for_url(lambda url: "/signin" not in url, timeout=10000)