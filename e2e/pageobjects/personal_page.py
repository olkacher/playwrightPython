"""PersonalPage handles the user's personal transactions."""

from playwright.sync_api import Page, Locator
from ..common.base_page import BasePage


class PersonalPage(BasePage):
    """Page object for the personal transactions page."""
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def open_first_transaction_with_note(self, note: str) -> None:
        """Opens the first transaction in the list."""
        self.page.locator("li", has_text=note).first.click()

