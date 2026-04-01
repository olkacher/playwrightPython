"""
Global pytest configuration for Playwright Python Example.

This example demonstrates:
- Authentication state management
- Page object fixtures
- Environment variable integration
- Multi-context test execution (public vs authenticated)
"""

import pytest
import os
from dotenv import load_dotenv

from config import (
    STORAGE_STATE,
    BASE_URL_ENV,
    DEFAULT_TIMEOUT_MS,
    TEST_USERNAME_ENV,
    DEFAULT_BASE_URL,
)

# Load environment variables
load_dotenv()

# Configuration (equivalent to baseURL and other settings)
BASE_URL = os.getenv(BASE_URL_ENV, DEFAULT_BASE_URL)

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Configure browser launch with settings from playwright.config.ts"""
    return {
        **browser_type_launch_args,
        "headless": True,                     # If false, a new browser window is opened for each test
        "args": ["--start-maximized"],        # Ensures the browser starts maximized
    }

@pytest.fixture(scope="function")
def page(page):
    """Configure page with settings from playwright.config.ts"""
    page.set_default_timeout(DEFAULT_TIMEOUT_MS)  # actionTimeout: 10000
    return page


@pytest.fixture(scope="function")
def browser_context_args(browser_context_args, request):
    """Configure browser context with application-specific settings."""
    context_args = {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900},
        "base_url": BASE_URL,
    }
    
    # Add authentication state for authenticated tests
    if request.node.get_closest_marker("authenticated"):
        # Check if storage state file exists
        if STORAGE_STATE.exists():
            context_args["storage_state"] = str(STORAGE_STATE)
        else:
            pytest.skip(f"Authentication state file {STORAGE_STATE} not found. Run authentication setup first.")
    
    return context_args

# Register global setup/teardown plugins
# Import the pytest hooks from global setup/teardown files
pytest_plugins = [
    "e2e.common.page_objects_fixture",
    "e2e.tests.authenticated.global.global_setup",
    "e2e.tests.authenticated.global.global_teardown",
]

# Global setup and teardown hooks 
def pytest_sessionstart(session):
    """
    Global test environment setup.
    Called once before all tests run.
    """
    print("Global test environment setup...")
    print(f"Target application: {BASE_URL}")
    print(f"Test user: {TEST_USERNAME_ENV}")

def pytest_sessionfinish(session, exitstatus):
    """
    Global test environment cleanup.
    Called once after all tests complete.
    """
    print("Global test environment cleanup...")