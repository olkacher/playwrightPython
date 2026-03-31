from playwright.sync_api import Page
from ..common.base_page import BasePage

class HomePage(BasePage):
    """Page object for the home page."""
    
    def __init__(self, page: Page):
        super().__init__(page)

    def goto(self):
        """Navigates to the home page."""
        self.page.goto("/")