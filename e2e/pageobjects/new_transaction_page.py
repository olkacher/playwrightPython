"""NewTransactionPage handles creating new transactions."""

from playwright.sync_api import Page, Locator
from ..common.base_page import BasePage


class NewTransactionPage(BasePage):
    """Page object for the new transaction page."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.input_user_search: Locator = page.locator("//input[@data-test='user-list-search-input']")
        self.list_item_first_user: Locator = page.locator("//ul[@data-test='users-list']/LI").first
        self.input_amount: Locator = page.locator("#amount")
        self.input_note: Locator = page.locator("#transaction-create-description-input")
        self.btn_pay: Locator = page.locator("//button[@data-test='transaction-create-submit-payment']")
    
    def select_contact(self, search_string: str) -> bool:
        """Selects a contact by searching and clicking the first result."""
        self.input_user_search.fill(search_string)
        first_contact_with_content = self.list_item_first_user.locator(f"//*[contains(text(), '{search_string}')]")
        # wait for the contact to be visible, click and return if amount input is visible
        first_contact_with_content.is_visible()
        self.list_item_first_user.click()
        return self.input_amount.is_visible()
    
    def set_payment_info(self, amount: str, note: str) -> None:
        """Sets the payment amount and note."""
        self.input_amount.fill(amount)
        self.input_note.fill(note)
    
    def submit_payment(self) -> None:
        """Submits the payment."""
        self.btn_pay.click()
    
    def is_alert_transaction_submitted_visible(self) -> bool:
        """Checks if the 'Transaction Submitted!' alert is visible."""
        alert_locator = self.page.locator("//div[contains(@class, 'Alert-message') and contains(text(), 'Transaction Submitted!')]")
        return alert_locator.is_visible()
    
    def is_amount_visible(self) -> bool:
        """Checks if the amount input is visible."""
        return self.input_amount.is_visible()