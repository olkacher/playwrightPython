"""Login and logout tests using direct Playwright API (without page objects)."""

import pytest
import re
import os
from playwright.sync_api import Page, expect

class TestLoginAndLogoutWithoutPageObjects:
    """Tests for login and logout using direct Playwright API calls."""
    
    def setup_method(self, method):
        """Setup before each test."""
        pass
    
    @pytest.mark.public
    def test_should_login_and_logout_successfully_without_page_objects(self, page: Page):
        """Verifies user can login and logout using direct selectors."""
        page.goto("/signin")
        expect(page).to_have_url(re.compile(r".*\/signin$"))
        
        page.fill('#username', os.getenv('TEST_USER_NAME'))
        page.fill('#password', os.getenv('TEST_PASSWORD'))
        page.click('[data-test="signin-submit"]')
        
        expected_username = f"@{os.getenv('TEST_USER_NAME')}"
        expect(page.locator('[data-test="sidenav-username"]')).to_have_text(expected_username)
                
        page.click("[data-test='sidenav-signout']")
        expect(page).to_have_url(re.compile(r".*\/signin$"))
    