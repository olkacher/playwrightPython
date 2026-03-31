"""Login and logout tests using page objects."""

import pytest
import os
import re
from playwright.sync_api import Page, expect


@pytest.mark.public
class TestLoginAndLogout:
    """Tests for login and logout functionality with page objects."""
    
    def setup_method(self, method):
        """Setup before each test."""
        pass
    
    def teardown_method(self, method):
        """Teardown after each test."""
        pass
    
    def test_should_login_and_logout_successfully(
            self, 
            page: Page, 
            sign_in_page, 
            side_menu_page
        ):

        """Verifies user can login and logout successfully."""
        sign_in_page.goto()
        expect(page).to_have_url(re.compile(r".*\/signin$"))
        
        sign_in_page.login(os.getenv("TEST_USER_NAME"), os.getenv("TEST_PASSWORD"))
        
        expected_username = f"@{os.getenv('TEST_USER_NAME')}"
        expect(side_menu_page.username).to_have_text(expected_username)
               
        side_menu_page.logout()
        expect(page).to_have_url(re.compile(r".*\/signin$"))
        