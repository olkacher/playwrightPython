"""
Global setup for authenticated tests.

Logs in a test user and stores browser authentication state
for tests that require an authenticated session.
"""

import os

from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

from config import (
    AUTH_DIR,
    STORAGE_STATE,
    BASE_URL_ENV,
    TEST_USERNAME_ENV,
    TEST_PASSWORD_ENV,
    DEFAULT_BASE_URL,
)
from e2e.pageobjects.sign_in_page import SignInPage

def global_setup() -> None:
    """
    Global setup function that logs in a user and stores authenticated browser state.
    
    This function:
    1. Launches a browser
    2. Navigates to the sign-in page
    3. Performs login with credentials from environment variables (using SignInPage pattern)
    4. Saves the authentication state to .auth/user.json
    5. Closes the browser
    
    """
    print("Global setup: Initially log in user and store authenticated browser state")
    load_dotenv()  # Load environment variables from .env file
    
    with sync_playwright() as p:
        # Launch browser, create isolated browser context (user session), and open a page
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        
        # Get credentials from environment
        username = os.getenv(TEST_USERNAME_ENV)
        password = os.getenv(TEST_PASSWORD_ENV)
        
        if not username or not password:
            raise ValueError(f"{TEST_USERNAME_ENV} and {TEST_PASSWORD_ENV} must be set in environment variables")
        
        # Navigate to sign-in page
        base_url = os.getenv(BASE_URL_ENV, DEFAULT_BASE_URL)
        signin_url = f"{base_url}/signin"
        page.goto(signin_url, wait_until='load')
        
        # Use SignInPage to handle login (DRY principle)
        sign_in_page = SignInPage(page)
        sign_in_page.login(username, password)
        sign_in_page.wait_until_logged_in()  
        
        # Ensure .auth directory exists
        AUTH_DIR.mkdir(parents=True, exist_ok=True)
        
        # Save session
        context.storage_state(path=str(STORAGE_STATE))        
        print(f"Authenticated browser state is stored in {STORAGE_STATE}")
        
        # Close the browser
        browser.close()

_setup_ran = False

def _needs_global_setup(items) -> bool:
    """Return True if at least one collected test requires authentication."""
    for item in items:
        # Preferred way: explicit marker
        if item.get_closest_marker("authenticated"):
            return True

        # Fallback for demo project structure
        if "authenticated" in str(item.fspath):
            return True

    return False

def pytest_collection_modifyitems(config, items):
    """
    Run global authentication setup only when collected tests require it.

    This hook is called after pytest collects test items.
    Setup runs when at least one collected test is marked as authenticated
    or belongs to the authenticated test area.
    """
    global _setup_ran

    if _setup_ran:
        return  # Avoid running setup multiple times
    
    if config.getoption("collectonly"):
        return  # Skip setup during collection-only runs

    if _needs_global_setup(items):
        print("Detected authenticated tests. Running global setup...")
        global_setup()
        _setup_ran = True

if __name__ == "__main__":
    # For direct execution, run global setup unconditionally
    global_setup()