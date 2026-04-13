"""
Login Page Object Model for InvenTree demo instance.

This module provides a LoginPage class that handles login functionality
for the InvenTree demo environment.
"""
from automation.ui.pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object Model for InvenTree Login Page.

    Inherits from BasePage to access common Playwright wrapper methods.
    """

    # Page URL
    LOGIN_URL = "https://demo.inventree.org/accounts/login/"

    # Locators
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = ".alert-danger, .errorlist"

    # Alternative locators (in case the above don't work)
    USERNAME_ALT = "#id_username"
    PASSWORD_ALT = "#id_password"
    SUBMIT_ALT = "input[type='submit'], button:has-text('Login'), button:has-text('Sign in')"

    def __init__(self, page):
        """
        Initialize LoginPage with Playwright page fixture.

        Args:
            page: Playwright page fixture from pytest
        """
        super().__init__(page)

    def navigate(self):
        """
        Navigate to the InvenTree demo login page.
        """
        self.navigate_to(self.LOGIN_URL)
        self.wait_for_load_state("domcontentloaded")

    def login(self, username: str, password: str):
        """
        Perform login action with provided credentials.

        This method enters the username and password, then clicks the login button.

        Args:
            username (str): Username for InvenTree demo
            password (str): Password for InvenTree demo

        Example:
            login_page = LoginPage(page)
            login_page.navigate()
            login_page.login("demo_user", "demo_password")
        """
        # Wait for login form to be visible
        self.wait_for_selector(self.USERNAME_INPUT)

        # Enter username
        self.enter_text(self.USERNAME_INPUT, username)

        # Enter password
        self.enter_text(self.PASSWORD_INPUT, password)

        # Click login button
        self.click_element(self.LOGIN_BUTTON)

        # Wait for navigation after login
        self.wait_for_load_state("networkidle")

    def login_with_demo_credentials(self):
        """
        Login using default InvenTree demo credentials.

        Note: Update these credentials based on the actual demo environment.
        Common demo credentials are typically username: 'admin', password: 'inventree'
        """
        demo_username = "admin"
        demo_password = "inventree"
        self.login(demo_username, demo_password)

    def is_login_page_loaded(self) -> bool:
        """
        Check if the login page is fully loaded.

        Returns:
            bool: True if login form is visible, False otherwise
        """
        return self.is_visible(self.USERNAME_INPUT) and self.is_visible(self.PASSWORD_INPUT)

    def get_error_message(self) -> str:
        """
        Get error message displayed on failed login.

        Returns:
            str: Error message text, or empty string if no error
        """
        if self.is_visible(self.ERROR_MESSAGE, timeout=3000):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def is_error_displayed(self) -> bool:
        """
        Check if login error message is displayed.

        Returns:
            bool: True if error message is visible, False otherwise
        """
        return self.is_visible(self.ERROR_MESSAGE, timeout=3000)

    def clear_login_form(self):
        """
        Clear username and password fields.
        """
        self.clear_and_enter_text(self.USERNAME_INPUT, "")
        self.clear_and_enter_text(self.PASSWORD_INPUT, "")

    def get_username_value(self) -> str:
        """
        Get the current value in the username field.

        Returns:
            str: Username field value
        """
        return self.get_attribute(self.USERNAME_INPUT, "value")

    def is_login_button_enabled(self) -> bool:
        """
        Check if the login button is enabled.

        Returns:
            bool: True if enabled, False otherwise
        """
        return self.is_enabled(self.LOGIN_BUTTON)

    def submit_login_form(self):
        """
        Submit the login form by pressing Enter key.

        Alternative to clicking the login button.
        """
        self.press_key(self.PASSWORD_INPUT, "Enter")
        self.wait_for_load_state("networkidle")
