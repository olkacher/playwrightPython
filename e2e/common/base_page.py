"""BasePage is the base class for all page objects."""

from abc import ABC, abstractmethod
from playwright.sync_api import Page



class BasePage(ABC):
    """Base class for all page objects. Provides common navigation and utility methods."""
    
    def __init__(self, page: Page) -> None:
        """Constructs a new BasePage with the given Playwright Page object."""
        self.page = page
    
    def get_current_url(self) -> str:
        """Returns the current URL of the page."""
        return self.page.url
    
    @abstractmethod
    def goto(self) -> None:
        """Navigate to the page. Must be implemented by subclasses."""
        pass
    
    def navigate_to(self, path: str) -> None:
        """Helper function to navigate to the given path."""
        self.page.goto(path, wait_until='load')

    def click_button(self, name: str) -> None:
        self.page.get_by_role("button", name=name).click()

    def click_tab(self, name: str) -> None:
        self.page.get_by_role("tab", name=name).click()
