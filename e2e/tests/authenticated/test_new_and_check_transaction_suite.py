"""Sequential transaction flow tests using pre-authenticated state."""

import pytest
import re
from playwright.sync_api import Page, expect


class TestTransactionFlowSuite:
    """Tests for creating and verifying transactions. Tests run sequentially with shared state."""
    
    AMOUNT = "57.00"
    NOTE = "test note"
    TRANSACTION_TESTUSER = "April"
    
    def setup_method(self, method):
        """Setup before each test."""
        pass
    
    @pytest.mark.authenticated
    def test_should_create_new_transaction(self, page: Page, top_menu_page, new_transaction_page, personal_page, transaction_detail_page,):
        """Creates a new transaction with contact selection and payment info."""
        page.goto("/")
        
        top_menu_page.click_new_transaction()
        expect(page).to_have_url(re.compile(r".*\/transaction\/new$"))
        
        success = new_transaction_page.select_contact(self.TRANSACTION_TESTUSER)
        assert success, f"Failed to select contact {self.TRANSACTION_TESTUSER}"
        
        amount_visible = new_transaction_page.is_amount_visible()
        assert amount_visible, "Amount field should be visible after selecting contact"
        
        new_transaction_page.set_payment_info(self.AMOUNT, self.NOTE)
        new_transaction_page.submit_payment()
        
        transaction_submitted = new_transaction_page.is_alert_transaction_submitted_visible()
        assert transaction_submitted, "Transaction submission alert should be visible"

        new_transaction_page.return_to_transactions()
        top_menu_page.navigate_to_tab_mine()
        expect(page).to_have_url(re.compile(r".*\/personal$"))
        
        personal_page.open_first_transaction()
        expect(page).to_have_url(re.compile(r".*\/transaction\/.*"))
        
        actual_amount = transaction_detail_page.get_transaction_amount()
        expected_amount = f"-${self.AMOUNT}"
        
        assert actual_amount == expected_amount, f"Expected amount {expected_amount}, but got {actual_amount}"
        
        page.screenshot(path="./e2e/reports/transaction_details.png", full_page=True)