"""
Global setup for authenticated tests.
This module provides global setup functionality that logs in a user and stores
the authenticated browser state for use in authenticated tests.
"""

import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from pytest_playwright.pytest_playwright import context
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
        # Launch browser
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
        
        # Ensure .auth directory exists
        AUTH_DIR.mkdir(parents=True, exist_ok=True)
        
        # Save session
        context.storage_state(path=str(STORAGE_STATE))        
        print(f"Authenticated browser state is stored in {STORAGE_STATE}")
        
        # Close the browser
        browser.close()


def pytest_configure(config):
    """
    Pytest configuration hook that runs the global setup.
    
    This function is automatically called by pytest during configuration
    and runs our authentication setup before any tests execute.
    
    Setup runs if:
    - Tests from authenticated/ directory are being run
    - Tests with @pytest.mark.authenticated marker are being run
    - Running tests from e2e/tests/ (includes authenticated tests)
    """
    # Check if we're running authenticated tests
    args = config.args
    run_setup = False
    
    # Check if any test path includes 'authenticated' or is a parent directory that includes authenticated tests
    for arg in args:
        arg_str = str(arg)
        if 'authenticated' in arg_str:
            run_setup = True
            break
        # If running from tests/ or e2e/tests/, assume authenticated tests are included
        if arg_str.endswith('tests') or arg_str.endswith('tests/') or arg_str.endswith('tests\\'):
            run_setup = True
            break
    
    # Check if marker expression includes 'authenticated'
    if config.getoption("markexpr", "") and "authenticated" in str(config.getoption("markexpr", "")):
        run_setup = True
    
    if run_setup:
        print("Running global authentication setup...")
        global_setup()


if __name__ == "__main__":
    # Allow running this script directly for testing
    global_setup()