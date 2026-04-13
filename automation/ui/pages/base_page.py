"""
Base Page class containing common Playwright wrapper methods.

This class provides reusable methods for common UI interactions
using Playwright, following the Page Object Model pattern.
"""
from playwright.sync_api import Page, expect


class BasePage:
    """
    Base page class with common Playwright wrapper methods.

    All page objects should inherit from this class to access
    common functionality and reduce code duplication.
    """

    def __init__(self, page: Page):
        """
        Initialize BasePage with Playwright page fixture.

        Args:
            page (Page): Playwright page fixture from pytest
        """
        self.page = page

    def navigate_to(self, url: str):
        """
        Navigate to a specific URL.

        Args:
            url (str): The URL to navigate to
        """
        self.page.goto(url)

    def wait_for_selector(self, selector: str, timeout: int = 30000):
        """
        Wait for an element to be visible on the page.

        Args:
            selector (str): CSS selector or text selector
            timeout (int): Maximum wait time in milliseconds (default: 30000)

        Returns:
            Locator: The located element
        """
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def click_element(self, selector: str, timeout: int = 30000):
        """
        Click on an element using Playwright's locator.

        Playwright automatically waits for the element to be actionable
        before clicking.

        Args:
            selector (str): CSS selector or text selector
            timeout (int): Maximum wait time in milliseconds (default: 30000)
        """
        self.page.locator(selector).click(timeout=timeout)

    def enter_text(self, selector: str, text: str, timeout: int = 30000):
        """
        Enter text into an input field using Playwright's fill method.

        Args:
            selector (str): CSS selector for the input field
            text (str): Text to enter
            timeout (int): Maximum wait time in milliseconds (default: 30000)
        """
        self.page.locator(selector).fill(text, timeout=timeout)

    def get_text(self, selector: str, timeout: int = 30000) -> str:
        """
        Get text content from an element.

        Args:
            selector (str): CSS selector or text selector
            timeout (int): Maximum wait time in milliseconds (default: 30000)

        Returns:
            str: Text content of the element
        """
        return self.page.locator(selector).text_content(timeout=timeout)

    def get_attribute(self, selector: str, attribute: str, timeout: int = 30000) -> str:
        """
        Get attribute value from an element.

        Args:
            selector (str): CSS selector
            attribute (str): Attribute name to retrieve
            timeout (int): Maximum wait time in milliseconds (default: 30000)

        Returns:
            str: Attribute value
        """
        return self.page.locator(selector).get_attribute(attribute, timeout=timeout)

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """
        Check if an element is visible on the page.

        Args:
            selector (str): CSS selector
            timeout (int): Maximum wait time in milliseconds (default: 5000)

        Returns:
            bool: True if visible, False otherwise
        """
        try:
            return self.page.locator(selector).is_visible(timeout=timeout)
        except Exception:
            return False

    def is_enabled(self, selector: str, timeout: int = 5000) -> bool:
        """
        Check if an element is enabled.

        Args:
            selector (str): CSS selector
            timeout (int): Maximum wait time in milliseconds (default: 5000)

        Returns:
            bool: True if enabled, False otherwise
        """
        try:
            return self.page.locator(selector).is_enabled(timeout=timeout)
        except Exception:
            return False

    def wait_for_url(self, url_pattern: str, timeout: int = 30000):
        """
        Wait for the page URL to match a pattern.

        Args:
            url_pattern (str): URL pattern to wait for (can use regex)
            timeout (int): Maximum wait time in milliseconds (default: 30000)
        """
        self.page.wait_for_url(url_pattern, timeout=timeout)

    def select_dropdown_option(self, selector: str, value: str, timeout: int = 30000):
        """
        Select an option from a dropdown by value.

        Args:
            selector (str): CSS selector for the select element
            value (str): Value to select
            timeout (int): Maximum wait time in milliseconds (default: 30000)
        """
        self.page.locator(selector).select_option(value, timeout=timeout)

    def check_checkbox(self, selector: str, timeout: int = 30000):
        """
        Check a checkbox element.

        Args:
            selector (str): CSS selector for the checkbox
            timeout (int): Maximum wait time in milliseconds (default: 30000)
        """
        self.page.locator(selector).check(timeout=timeout)

    def uncheck_checkbox(self, selector: str, timeout: int = 30000):
        """
        Uncheck a checkbox element.

        Args:
            selector (str): CSS selector for the checkbox
            timeout (int): Maximum wait time in milliseconds (default: 30000)
        """
        self.page.locator(selector).uncheck(timeout=timeout)

    def press_key(self, selector: str, key: str, timeout: int = 30000):
        """
        Press a keyboard key on an element.

        Args:
            selector (str): CSS selector for the element
            key (str): Key to press (e.g., 'Enter', 'Escape', 'Tab')
            timeout (int): Maximum wait time in milliseconds (default: 30000)
        """
        self.page.locator(selector).press(key, timeout=timeout)

    def get_page_title(self) -> str:
        """
        Get the current page title.

        Returns:
            str: Page title
        """
        return self.page.title()

    def get_current_url(self) -> str:
        """
        Get the current page URL.

        Returns:
            str: Current URL
        """
        return self.page.url

    def scroll_to_element(self, selector: str, timeout: int = 30000):
        """
        Scroll to an element on the page.

        Args:
            selector (str): CSS selector
            timeout (int): Maximum wait time in milliseconds (default: 30000)
        """
        self.page.locator(selector).scroll_into_view_if_needed(timeout=timeout)

    def take_screenshot(self, path: str):
        """
        Take a screenshot of the current page.

        Args:
            path (str): File path to save the screenshot
        """
        self.page.screenshot(path=path)

    def wait_for_load_state(self, state: str = "load", timeout: int = 30000):
        """
        Wait for a specific load state.

        Args:
            state (str): Load state to wait for ('load', 'domcontentloaded', 'networkidle')
            timeout (int): Maximum wait time in milliseconds (default: 30000)
        """
        self.page.wait_for_load_state(state, timeout=timeout)

    def get_element_count(self, selector: str) -> int:
        """
        Get the count of elements matching the selector.

        Args:
            selector (str): CSS selector

        Returns:
            int: Number of matching elements
        """
        return self.page.locator(selector).count()

    def hover_element(self, selector: str, timeout: int = 30000):
        """
        Hover over an element.

        Args:
            selector (str): CSS selector
            timeout (int): Maximum wait time in milliseconds (default: 30000)
        """
        self.page.locator(selector).hover(timeout=timeout)

    def double_click_element(self, selector: str, timeout: int = 30000):
        """
        Double-click on an element.

        Args:
            selector (str): CSS selector
            timeout (int): Maximum wait time in milliseconds (default: 30000)
        """
        self.page.locator(selector).dblclick(timeout=timeout)

    def right_click_element(self, selector: str, timeout: int = 30000):
        """
        Right-click (context click) on an element.

        Args:
            selector (str): CSS selector
            timeout (int): Maximum wait time in milliseconds (default: 30000)
        """
        self.page.locator(selector).click(button="right", timeout=timeout)

    def clear_and_enter_text(self, selector: str, text: str, timeout: int = 30000):
        """
        Clear existing text and enter new text.

        Args:
            selector (str): CSS selector for the input field
            text (str): Text to enter
            timeout (int): Maximum wait time in milliseconds (default: 30000)
        """
        locator = self.page.locator(selector)
        locator.clear(timeout=timeout)
        locator.fill(text, timeout=timeout)

    def expect_element_visible(self, selector: str):
        """
        Assert that an element is visible using Playwright's expect API.

        Args:
            selector (str): CSS selector
        """
        expect(self.page.locator(selector)).to_be_visible()

    def expect_element_has_text(self, selector: str, text: str):
        """
        Assert that an element contains specific text.

        Args:
            selector (str): CSS selector
            text (str): Expected text content
        """
        expect(self.page.locator(selector)).to_have_text(text)

    def expect_url_contains(self, url_fragment: str):
        """
        Assert that the current URL contains a specific fragment.

        Args:
            url_fragment (str): URL fragment to check for
        """
        expect(self.page).to_have_url(url_fragment)
