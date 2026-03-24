"""Pytest fixtures for page objects. Automatically injects page objects into tests."""

import pytest
from playwright.sync_api import Page

from e2e.pageobjects.sign_in_page import SignInPage
from e2e.pageobjects.side_menu_page import SideMenuPage
from e2e.pageobjects.top_menu_page import TopMenuPage
from e2e.pageobjects.new_transaction_page import NewTransactionPage
from e2e.pageobjects.personal_page import PersonalPage
from e2e.pageobjects.transaction_detail_page import TransactionDetailPage


@pytest.fixture
def sign_in_page(page: Page) -> SignInPage:
    """Provides a SignInPage instance."""
    return SignInPage(page)


@pytest.fixture
def side_menu_page(page: Page) -> SideMenuPage:
    """Provides a SideMenuPage instance."""
    return SideMenuPage(page)


@pytest.fixture
def top_menu_page(page: Page) -> TopMenuPage:
    """Provides a TopMenuPage instance."""
    return TopMenuPage(page)


@pytest.fixture
def new_transaction_page(page: Page) -> NewTransactionPage:
    """Provides a NewTransactionPage instance."""
    return NewTransactionPage(page)


@pytest.fixture
def personal_page(page: Page) -> PersonalPage:
    """Provides a PersonalPage instance."""
    return PersonalPage(page)


@pytest.fixture
def transaction_detail_page(page: Page) -> TransactionDetailPage:
    """Provides a TransactionDetailPage instance."""
    return TransactionDetailPage(page)