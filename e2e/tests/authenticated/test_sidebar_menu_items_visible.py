"""Test sidebar menu items visibility using pre-authenticated state."""

import os
import pytest
from playwright.sync_api import Page, expect
from e2e.common.assertion_helpers import (
    assert_all,
    check_contains_text,
    check_enabled,
    check_not_empty,
    check_text,
    check_visible,
)

class TestSidebarMenuItemsVisible:
    """Test sidebar menu items visibility. Assumes user is already authenticated."""
    USER_FULL_NAME = "Lenore L S"

    def setup_method(self, method):
        """Setup before each test."""
        pass

    @pytest.mark.authenticated
    def test_sidebar_menu_items_visible(self, page: Page, side_menu_page, home_page):
        """Verifies sidebar menu items are visible for authenticated user."""
        
        username = os.getenv("TEST_USER_NAME")

        home_page.goto()

        checks = [
            # Sidebar
            check_visible("Sidebar", side_menu_page.sidebar),

            # User Info
            check_visible("User Avatar", side_menu_page.avatar),
            check_visible("User Full Name", side_menu_page.user_full_name),
            check_text("User Full Name Text", side_menu_page.user_full_name, self.USER_FULL_NAME),
            check_visible("Username", side_menu_page.username),
            check_contains_text("Username Text", side_menu_page.username, "@" + username),

            # Balance Info
            check_visible("Balance", side_menu_page.balance),
            check_not_empty("Balance Not Empty", side_menu_page.balance),
            check_visible("Balance Label", side_menu_page.balance_label),
        ]

        # Verify menu items are visible
        menu_items = ["Home", "My Account", "Bank Accounts", "Notifications", "Logout"]

        for item in menu_items:
            button = side_menu_page.menu_button(item)
            icon = side_menu_page.menu_icon(item)

            checks.extend([
                check_visible(f"Menu button '{item}'", button),
                check_enabled(f"Menu button '{item}'", button),
                check_contains_text(f"Menu button '{item}' text", button, item),
                check_visible(f"Menu icon '{item}'", icon),
            ])

        assert_all(checks)