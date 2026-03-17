"""PersonalPage handles the user's personal transactions."""

from playwright.sync_api import Page, Locator
from ..common.base_page import BasePage


class PersonalPage(BasePage):
    """Page object for the personal transactions page."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.link_first_transaction_item: Locator = page.locator("//li[starts-with(@data-test, 'transaction-item-')]").first
    
    def open_first_transaction(self) -> None:
        """Opens the first transaction in the list."""
        self.link_first_transaction_item.click()