"""
Global setup for authenticated tests.

Logs in a test user and stores browser authentication state
for tests that require an authenticated session.
"""

import os

from dotenv import load_dotenv
from playwright.sync_api import Playwright, BrowserType, sync_playwright

from config import (
    AUTH_DIR,
    STORAGE_STATE,
    BASE_URL_ENV,
    TEST_USERNAME_ENV,
    TEST_PASSWORD_ENV,
    DEFAULT_BASE_URL,
)
from e2e.pageobjects.sign_in_page import SignInPage


DEFAULT_BROWSER = "chromium"
SUPPORTED_BROWSERS = {"chromium", "firefox", "webkit"}

_setup_ran = False


def _get_required_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Environment variable '{var_name}' must be set")
    return value


def _get_browser_launcher(playwright: Playwright, browser_name: str) -> BrowserType:
    browser_name = browser_name.strip().lower()

    if browser_name not in SUPPORTED_BROWSERS:
        raise ValueError(
            f"Unsupported browser: {browser_name}. "
            f"Supported browsers: {', '.join(sorted(SUPPORTED_BROWSERS))}"
        )

    return getattr(playwright, browser_name)


def global_setup(browser_name: str = DEFAULT_BROWSER) -> None:
    """
    Log in a user and store authenticated browser state.

    Args:
        browser_name: Browser type to use for setup
                      (chromium, firefox, webkit)
    """
    load_dotenv()

    username = _get_required_env(TEST_USERNAME_ENV)
    password = _get_required_env(TEST_PASSWORD_ENV)
    base_url = os.getenv(BASE_URL_ENV, DEFAULT_BASE_URL)

    AUTH_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Global setup: running with browser '{browser_name}'")
    print("Global setup: log in user and store authenticated browser state")

    with sync_playwright() as playwright:
        browser_launcher = _get_browser_launcher(playwright, browser_name)
        browser = browser_launcher.launch()
        context = browser.new_context()
        page = context.new_page()

        try:
            signin_url = f"{base_url}/signin"
            page.goto(signin_url, wait_until="load")

            sign_in_page = SignInPage(page)
            sign_in_page.login(username, password)
            sign_in_page.wait_until_logged_in()

            context.storage_state(path=str(STORAGE_STATE))
            print(f"Authenticated browser state is stored in {STORAGE_STATE}")
        finally:
            context.close()
            browser.close()


def _needs_global_setup(items) -> bool:
    """Return True if at least one collected test requires authentication."""
    for item in items:
        if item.get_closest_marker("authenticated"):
            return True

        if "authenticated" in str(item.fspath):
            return True

    return False


def pytest_collection_modifyitems(config, items):
    """
    Run global authentication setup only when collected tests require it.
    """
    global _setup_ran

    if _setup_ran:
        return

    if config.getoption("collectonly"):
        return

    if not _needs_global_setup(items):
        return

    # pytest-playwright supports --browser and exposes browser_name fixture.
    # Here we read the selected browser from pytest option.
    selected_browsers = config.getoption("browser") or [DEFAULT_BROWSER]
    browser_name = selected_browsers[0]

    print("Detected authenticated tests. Running global setup...")
    global_setup(browser_name=browser_name)
    _setup_ran = True


if __name__ == "__main__":
    global_setup()