"""Test sidebar menu items visibility using pre-authenticated state."""

import os

import pytest
from playwright.sync_api import Page, expect

from e2e.common.page_objects_fixture import side_menu_page

class TestSidebarMenuItemsVisible:
    """Test sidebar menu items visibility. Assumes user is already authenticated."""
    USER_FULL_NAME = "Lenore L S"

    def setup_method(self, method):
        """Setup before each test."""
        pass

    @pytest.mark.authenticated
    def test_sidebar_menu_items_visible(self, page: Page, side_menu_page):
        """Verifies sidebar menu items are visible for authenticated user."""
        
        username = os.getenv("TEST_USER_NAME")

        page.goto("/")
        
        # Verify sidebar is visible
        expect(side_menu_page.sidebar).to_be_visible()
        
        # Verify user info is visible
        expect(side_menu_page.avatar).to_be_visible()
        expect(side_menu_page.user_full_name).to_be_visible()
        expect(side_menu_page.user_full_name).to_have_text(self.USER_FULL_NAME)
        expect(side_menu_page.username).to_be_visible()
        expect(side_menu_page.username).to_contain_text("@" + username)
        
        # Verify balance info is visible
        expect(side_menu_page.balance).to_be_visible()
        expect(side_menu_page.balance).not_to_be_empty()
        expect(side_menu_page.balance_label).to_be_visible()

        # Verify menu items are visible
        menu_items = ["Home", "My Account", "Bank Accounts", "Notifications", "Logout"]

        for item in menu_items:
            button = side_menu_page.menu_button(item)
            icon = side_menu_page.menu_icon(item)

            expect(button).to_be_visible()
            expect(button).to_be_enabled()
            expect(button).to_contain_text(item)
            expect(icon).to_be_visible()