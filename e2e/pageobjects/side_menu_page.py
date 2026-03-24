"""SideMenuPage handles side menu navigation and user actions."""

from playwright.sync_api import Page, Locator
from typing import Optional
from ..common.base_page import BasePage


class SideMenuPage(BasePage):
    """Page object for the side menu."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.div_username: Locator = page.locator("//div[contains(@class, 'Grid-item')]//*[@data-test='sidenav-username']")
    
    def get_username(self) -> Optional[str]:
        """Returns the username displayed in the side menu."""
        return self.div_username.text_content()
    
    def logout(self) -> None:
        """Logs out the user."""
        self.click_button("Sign Out")