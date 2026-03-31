"""TopMenuPage handles top navigation menu actions."""

from playwright.sync_api import Page, Locator
from ..common.base_page import BasePage


class TopMenuPage(BasePage):
    """Page object for the top navigation menu."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.a_new_transaction: Locator = page.get_by_role("button", name="New")
    
    def goto(self):
        raise NotImplementedError("TopMenuPage cannot be opened directly")
    
    def navigate_to_tab_mine(self) -> None:
        """Navigates to the 'My Transactions' tab."""
        self.click_tab("Mine")