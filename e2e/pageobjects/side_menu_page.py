"""SideMenuPage handles side menu navigation and user actions."""

from os import name

from playwright.sync_api import Page
from ..common.base_page import BasePage


class SideMenuPage(BasePage):
    """Page object for the side menu."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.sidebar = page.locator('[data-test="sidenav"]')

        self.avatar = self.sidebar.get_by_role("img")
        self.user_full_name = page.locator('[data-test="sidenav-user-full-name"]')
        self.username = page.locator('[data-test="sidenav-username"]')

        self.balance = page.locator('[data-test="sidenav-user-balance"]')
        self.balance_label = self.sidebar.get_by_role("heading", name="Account Balance")
    
    def goto(self):
        raise NotImplementedError("SideMenuPage cannot be opened directly")
    
    def logout(self) -> None:
        """Logs out the user."""
        self.click_button("Logout")

    def menu_button(self, name: str):
        return self.sidebar.get_by_role("button", name=name)

    def menu_icon(self, name: str):
        return self.menu_button(name).locator("svg")
    
    