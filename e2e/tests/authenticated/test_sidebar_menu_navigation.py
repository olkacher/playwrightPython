"""Transaction flow tests using pre-authenticated state."""

import pytest
import re
from playwright.sync_api import Page, expect

class TestSidebarMenuNavigation:
    """Test sidebar menu navigation. Assumes user is already authenticated."""

    @pytest.mark.authenticated
    def test_sidebar_menu_navigation(self, page: Page, side_menu_page, home_page):
        """Verifies sidebar menu navigation for authenticated user."""

        home_page.goto()
        
        # Define expected URLs for each menu item
        expected_urls = {
            "Home": re.compile(r".*\/$"),
            "My Account": re.compile(r".*\/user\/settings$"),
            "Bank Accounts": re.compile(r".*\/bankaccounts$"),
            "Notifications": re.compile(r".*\/notifications$"),
        }

        # Test navigation for each menu item except Logout
        for item, url_pattern in expected_urls.items():
            button = side_menu_page.menu_button(item)
            button.click()
            expect(page).to_have_url(url_pattern)


