"""NewTransactionPage handles creating new transactions."""

from playwright.sync_api import Page, Locator
from ..common.base_page import BasePage


class NewTransactionPage(BasePage):
    """Page object for the new transaction page."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.input_user_search: Locator = page.get_by_role("textbox", name="Search")
        self.input_amount: Locator = page.get_by_role("textbox", name="Amount")
        self.input_note: Locator = page.get_by_role("textbox", name="Note")
    
    def select_contact(self, search_string: str) -> bool:
        """Selects a contact by searching and clicking the first result."""
        self.input_user_search.fill(search_string)
        contact = self.page.get_by_role("listitem").filter(has_text=search_string).first
        contact.click()
        return self.input_amount.is_visible()
    
    def set_payment_info(self, amount: str, note: str) -> None:
        """Sets the payment amount and note."""
        self.input_amount.fill(amount)
        self.input_note.fill(note)
    
    def submit_payment(self) -> None:
        """Submits the payment."""
        self.click_button("Pay")

    def return_to_transactions(self) -> None:
        """Returns to the transactions page."""
        self.click_button("Return To Transactions")
    
    def is_alert_transaction_submitted_visible(self) -> bool:
        """Checks if the 'Transaction Submitted!' alert is visible."""
        alert_locator = self.page.locator("//div[contains(@class, 'Alert-message') and contains(text(), 'Transaction Submitted!')]")
        return alert_locator.is_visible()
    
    def is_amount_visible(self) -> bool:
        """Checks if the amount input is visible."""
        return self.input_amount.is_visible()