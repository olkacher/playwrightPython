"""TransactionDetailPage handles transaction detail view."""

from playwright.sync_api import Page, Locator
from typing import Optional
from ..common.base_page import BasePage


class TransactionDetailPage(BasePage):
    """Page object for the transaction detail page."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.span_transaction_amount: Locator = page.locator("//span[contains(@data-test, 'transaction-amount')]")
    
    def get_transaction_amount(self) -> Optional[str]:
        """Returns the transaction amount."""
        return self.span_transaction_amount.text_content()