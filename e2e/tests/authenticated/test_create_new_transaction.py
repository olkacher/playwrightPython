"""Transaction flow tests using pre-authenticated state."""

import pytest
import re
from playwright.sync_api import Page, expect

from e2e.common.page_objects_fixture import new_transaction_page, transaction_detail_page


class TestTransactionFlowSuite:
    """Test for creating and verifying transactions. Assumes user is already authenticated."""
    
    AMOUNT = "57.00"
    NOTE = "test note"
    TRANSACTION_TESTUSER = "April"
    
    def setup_method(self, method):
        """Setup before each test."""
        pass
    
    @pytest.mark.authenticated
    def test_should_create_new_pay_transaction(
        self, 
        page: Page, 
        top_menu_page, 
        new_transaction_page, 
        personal_page, 
        transaction_detail_page,
    ):
        """Verifies user can create a new payment transaction."""

        page.goto("/")
        
        top_menu_page.click_new_transaction()
        expect(page).to_have_url(re.compile(r".*\/transaction\/new$"))
        
        new_transaction_page.select_contact(self.TRANSACTION_TESTUSER)
        expect(new_transaction_page.amount_input).to_be_visible()
        
        new_transaction_page.set_payment_info(self.AMOUNT, self.NOTE)
        new_transaction_page.submit_payment()
        expect(new_transaction_page.alert_transaction_submitted).to_be_visible()

        new_transaction_page.return_to_transactions()
        top_menu_page.navigate_to_tab_mine()
        expect(page).to_have_url(re.compile(r".*\/personal$"))
        
        personal_page.open_first_transaction_with_note(self.NOTE)
        expect(page).to_have_url(re.compile(r".*\/transaction\/.*"))
        
        expect(transaction_detail_page.transaction_amount).to_have_text(f"-${self.AMOUNT}")

    @pytest.mark.authenticated
    def test_should_create_new_request_transaction(
        self, 
        page: Page, 
        top_menu_page, 
        new_transaction_page, 
        personal_page, 
        transaction_detail_page,
    ):
        """Verifies user can create a new request transaction."""

        page.goto("/")
        
        top_menu_page.click_new_transaction()
        expect(page).to_have_url(re.compile(r".*\/transaction\/new$"))
        
        new_transaction_page.select_contact(self.TRANSACTION_TESTUSER)
        expect(new_transaction_page.amount_input).to_be_visible()
        
        new_transaction_page.set_payment_info(self.AMOUNT, self.NOTE)
        new_transaction_page.submit_request()
        expect(new_transaction_page.alert_transaction_submitted).to_be_visible()

        new_transaction_page.return_to_transactions()
        top_menu_page.navigate_to_tab_mine()
        expect(page).to_have_url(re.compile(r".*\/personal$"))
        
        personal_page.open_first_transaction_with_note(self.NOTE)
        expect(page).to_have_url(re.compile(r".*\/transaction\/.*"))
        
        expect(transaction_detail_page.transaction_amount).to_have_text(f"+${self.AMOUNT}")    