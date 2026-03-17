"""SignInPage handles login functionality."""

from playwright.sync_api import Page, Locator
from e2e.common.base_page import BasePage


class SignInPage(BasePage):
    """Page object for the sign-in page."""
    
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.input_username: Locator = page.locator('#username')
        self.input_password: Locator = page.locator('#password')
        self.btn_sign_in: Locator = page.locator('//button[@data-test="signin-submit"]')
    
    def goto(self) -> None:
        """Navigate to the sign-in page."""
        self.navigate_to("/signin")
    
    def login(self, username: str, password: str) -> None:
        """Login with the provided username and password."""
        self.input_username.fill(username)
        self.input_password.fill(password)
        self.btn_sign_in.click()