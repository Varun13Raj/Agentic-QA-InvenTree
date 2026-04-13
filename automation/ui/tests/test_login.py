"""
Login functionality tests for InvenTree UI using Playwright.

This module tests the login flow for InvenTree demo instance
using the Page Object Model pattern.
"""
import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import pytest
from playwright.sync_api import Page, expect
from automation.ui.pages.login_page import LoginPage


def test_successful_login(page: Page):
    """
    Test successful login with valid demo credentials.

    This test verifies that a user can successfully log in to the
    InvenTree demo instance using valid credentials.

    Args:
        page (Page): Playwright page fixture from pytest-playwright

    Test Steps:
        1. Navigate to login page
        2. Enter valid username and password
        3. Click login button
        4. Verify successful login by checking URL change

    Expected Result:
        User is logged in and redirected away from login page
    """
    # Instantiate LoginPage with page fixture
    login_page = LoginPage(page)

    # Navigate to the login page
    login_page.navigate()

    # Verify login page is loaded
    assert login_page.is_login_page_loaded(), "Login page did not load properly"

    # Perform login with demo credentials
    login_page.login_with_demo_credentials()

    # Assertion 1: Verify URL has changed (no longer on login page)
    current_url = login_page.get_current_url()
    assert "/web/login" not in current_url, \
        f"Still on login page after login attempt. Current URL: {current_url}"

    # Assertion 2: Verify we're on a valid InvenTree page (not login)
    assert "demo.inventree.org" in current_url, \
        f"Not on InvenTree domain. Current URL: {current_url}"

    # Additional assertion: Check page title changed
    page_title = login_page.get_page_title()
    assert page_title != "Login", \
        f"Page title still shows Login. Current title: {page_title}"


def test_successful_login_with_explicit_credentials(page: Page):
    """
    Test successful login with explicitly provided credentials.

    Args:
        page (Page): Playwright page fixture from pytest-playwright

    Test Steps:
        1. Navigate to login page
        2. Enter username and password explicitly
        3. Submit login form
        4. Verify successful authentication
    """
    login_page = LoginPage(page)
    login_page.navigate()

    # Login with explicit credentials
    login_page.login("admin", "inventree")

    # Verify login success by checking URL
    current_url = page.url
    assert "/web/login" not in current_url, \
        "Login failed - still on login page"


def test_login_page_elements_visible(page: Page):
    """
    Test that all required login page elements are visible.

    Args:
        page (Page): Playwright page fixture from pytest-playwright

    Test Steps:
        1. Navigate to login page
        2. Verify username field is visible
        3. Verify password field is visible
        4. Verify login button is visible and enabled
    """
    login_page = LoginPage(page)
    login_page.navigate()

    # Verify all login form elements are present
    assert login_page.is_visible(login_page.USERNAME_INPUT), \
        "Username input field not visible"
    assert login_page.is_visible(login_page.PASSWORD_INPUT), \
        "Password input field not visible"
    assert login_page.is_visible(login_page.LOGIN_BUTTON), \
        "Login button not visible"

    # Verify login button is enabled
    assert login_page.is_login_button_enabled(), \
        "Login button is not enabled"


@pytest.mark.parametrize("username,password,should_fail", [
    ("invalid_user", "wrong_password", True),
    ("admin", "wrong_password", True),
    ("", "", True),
])
def test_login_with_invalid_credentials(page: Page, username, password, should_fail):
    """
    Test login with invalid credentials.

    This test verifies that login fails with invalid credentials
    and appropriate error handling occurs.

    Args:
        page (Page): Playwright page fixture
        username (str): Username to test
        password (str): Password to test
        should_fail (bool): Expected to fail flag
    """
    login_page = LoginPage(page)
    login_page.navigate()

    # Attempt login with invalid credentials
    login_page.login(username, password)

    if should_fail:
        # Verify still on login page or error is shown
        current_url = login_page.get_current_url()
        # Either still on login page OR error message is displayed
        is_still_on_login = "/web/login" in current_url or "/login" in current_url
        has_error = login_page.is_error_displayed()

        assert is_still_on_login or has_error, \
            f"Expected login to fail but no error detected. URL: {current_url}"


def test_login_form_submission_with_enter_key(page: Page):
    """
    Test login form submission using Enter key.

    Args:
        page (Page): Playwright page fixture

    Test Steps:
        1. Navigate to login page
        2. Enter credentials
        3. Press Enter key in password field
        4. Verify login success
    """
    login_page = LoginPage(page)
    login_page.navigate()

    # Enter credentials
    login_page.enter_text(login_page.USERNAME_INPUT, "admin")
    login_page.enter_text(login_page.PASSWORD_INPUT, "inventree")

    # Submit using Enter key
    login_page.submit_login_form()

    # Verify login success
    current_url = login_page.get_current_url()
    assert "/web/login" not in current_url, \
        "Login with Enter key failed"


def test_clear_login_form(page: Page):
    """
    Test clearing the login form fields.

    Args:
        page (Page): Playwright page fixture

    Test Steps:
        1. Navigate to login page
        2. Enter credentials
        3. Clear the form
        4. Verify fields are empty
    """
    login_page = LoginPage(page)
    login_page.navigate()

    # Enter some text
    login_page.enter_text(login_page.USERNAME_INPUT, "testuser")
    login_page.enter_text(login_page.PASSWORD_INPUT, "testpass")

    # Clear the form
    login_page.clear_login_form()

    # Verify fields are cleared
    username_value = login_page.get_username_value()
    assert username_value == "" or username_value is None, \
        f"Username field not cleared. Value: {username_value}"


def test_login_page_url_navigation(page: Page):
    """
    Test direct navigation to login page URL.

    Args:
        page (Page): Playwright page fixture

    Test Steps:
        1. Navigate directly to login URL
        2. Verify page loads correctly
        3. Verify correct URL
    """
    login_page = LoginPage(page)
    login_page.navigate()

    # Verify URL is correct
    current_url = login_page.get_current_url()
    assert login_page.LOGIN_URL in current_url, \
        f"Not on login page. Expected: {login_page.LOGIN_URL}, Got: {current_url}"

    # Verify login page is loaded
    assert login_page.is_login_page_loaded(), \
        "Login page elements not loaded properly"
