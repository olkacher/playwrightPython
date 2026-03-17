"""BasePage is the base class for all page objects."""

from playwright.sync_api import Page


class BasePage:
    """Base class for all page objects. Provides common navigation and utility methods."""
    
    def __init__(self, page: Page) -> None:
        """Constructs a new BasePage with the given Playwright Page object."""
        self.page = page
    
    def get_current_url(self) -> str:
        """Returns the current URL of the page."""
        return self.page.url
    
    def goto(self) -> None:
        """Open the expected page. Should be overridden by subclasses."""
        self.navigate_to("/")
    
    def navigate_to(self, path: str) -> None:
        """Helper function to navigate to the given path."""
        self.page.goto(path, wait_until='load')
