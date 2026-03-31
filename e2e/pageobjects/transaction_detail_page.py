"""TransactionDetailPage handles transaction detail view."""

from playwright.sync_api import Page, Locator
from ..common.base_page import BasePage


class TransactionDetailPage(BasePage):
    """Page object for the transaction detail page."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.transaction_amount: Locator = page.locator('[data-test^="transaction-amount-"]')
    
    def goto(self) -> None:
        raise NotImplementedError
    ("TransactionDetailPage does not support direct navigation without a transaction ID. "
    "Open it via transaction list.")