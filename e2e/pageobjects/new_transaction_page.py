"""NewTransactionPage handles creating new transactions."""

from playwright.sync_api import Page, Locator
from ..common.base_page import BasePage


class NewTransactionPage(BasePage):
    """Page object for the new transaction page."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.user_search_input: Locator = page.get_by_role("textbox", name="Search")
        self.amount_input: Locator = page.get_by_role("textbox", name="Amount")
        self.note_input: Locator = page.get_by_role("textbox", name="Note")
        self.alert_transaction_submitted: Locator = page.get_by_role("alert").filter(has_text="Transaction Submitted!")
    
    def goto(self) -> None:
        """Navigate to the new transaction page."""
        self.navigate_to("/transaction/new")
        
    def select_contact(self, search_string: str) -> None:
        """Search for a contact and select the first matching result."""
        self.user_search_input.fill(search_string)
        contact = self.page.get_by_role("listitem").filter(has_text=search_string).first
        contact.click()
    
    def set_payment_info(self, amount: str, note: str) -> None:
        """Sets the payment amount and note."""
        self.amount_input.fill(amount)
        self.note_input.fill(note)
    
    def submit_payment(self) -> None:
        """Submits the payment."""
        self.click_button("Pay")

    def submit_request(self) -> None:
        """Submits the request."""
        self.click_button("Request")
    
    def return_to_transactions(self) -> None:
        """Returns to the transactions page."""
        self.click_button("Return To Transactions") 
