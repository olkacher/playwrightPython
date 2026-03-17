"""Additional synchronization utilities for Playwright.

Note: Playwright has built-in auto-wait that handles most synchronization needs.
Use these utilities only when additional synchronization is required for specific frameworks.
"""

from playwright.sync_api import Page


class BrowserSyncUtils:
    """Provides additional synchronization utilities for jQuery and Angular applications."""
    
    def __init__(self, page: Page) -> None:
        """Constructs a new BrowserSyncUtils with the given Playwright Page object."""
        self.page = page
    
    def wait_for_page_load(self, timeout: int = 30000) -> None:
        """Wait until the DOM is fully loaded (default timeout: 30 seconds)."""
        self.page.wait_for_load_state('load', timeout=timeout)
    
    def wait_for_jquery(self) -> None:
        """Wait until all jQuery requests are completed."""
        self.page.wait_for_function("""() => {
            return window.jQuery && window.jQuery.active === 0;
        }""")
    
    def wait_for_angular(self) -> None:
        """Wait until all Angular requests are completed."""
        self.page.wait_for_function("""() => {
            return (
                window.angular &&
                window.angular.element(document).injector().get('$http').pendingRequests.length === 0
            );
        }""")