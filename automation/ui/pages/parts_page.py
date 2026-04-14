"""
Parts Page Object Model for InvenTree.

This module provides a PartsPage class that handles interactions
with the Parts module in InvenTree.
"""
from automation.ui.pages.base_page import BasePage


class PartsPage(BasePage):
    """
    Page Object Model for InvenTree Parts Page.

    Inherits from BasePage to access common Playwright wrapper methods.
    """

    # Page URL (Updated to use local Docker instance)
    PARTS_URL = "http://localhost:8000/web/part"

    # Navigation Locators
    PARTS_NAV_LINK = "a:has-text('Parts')"
    PARTS_NAV_LINK_ALT = "nav a[href*='part'], [role='navigation'] a:has-text('Parts')"

    # Parts List Page Locators
    NEW_PART_BUTTON = "button:has-text('New Part')"
    NEW_PART_BUTTON_ALT = "button[aria-label*='New Part'], button[title*='New Part'], .btn:has-text('Add Part')"

    # Part Creation Form Locators
    PART_NAME_INPUT = "input[name='name']"
    PART_NAME_INPUT_ALT = "input[id*='name'], input[placeholder*='Name' i]"

    PART_DESCRIPTION_INPUT = "textarea[name='description']"
    PART_DESCRIPTION_INPUT_ALT = "textarea[id*='description'], textarea[placeholder*='Description' i]"

    PART_CATEGORY_SELECT = "select[name='category']"

    SUBMIT_BUTTON = "button[type='submit']"
    SUBMIT_BUTTON_ALT = "button:has-text('Save'), button:has-text('Create'), button:has-text('Submit')"

    CANCEL_BUTTON = "button:has-text('Cancel')"

    # Parts List Locators
    PARTS_TABLE = "table, .table, [role='table']"
    PART_ROW = "tr, .part-row, [role='row']"

    # Stock Management Locators
    STOCK_TAB = "a:has-text('Stock'), button:has-text('Stock'), [role='tab']:has-text('Stock')"
    STOCK_TAB_ALT = "[data-testid='stock-tab'], .nav-link:has-text('Stock'), [href*='stock']"

    ADD_STOCK_BUTTON = "button:has-text('Add Stock'), button:has-text('New Stock Item')"
    ADD_STOCK_BUTTON_ALT = "button[aria-label*='Add Stock'], button[title*='Add Stock'], .btn:has-text('Create Stock')"

    STOCK_QUANTITY_INPUT = "input[name='quantity']"
    STOCK_QUANTITY_INPUT_ALT = "input[id*='quantity'], input[placeholder*='Quantity' i]"

    def __init__(self, page):
        """
        Initialize PartsPage with Playwright page fixture.

        Args:
            page: Playwright page fixture from pytest
        """
        super().__init__(page)

    def navigate_to_parts(self):
        """
        Navigate directly to the Parts page URL.

        This is a direct navigation method.
        """
        self.navigate_to(self.PARTS_URL)
        self.wait_for_load_state("networkidle")
        # Wait for dynamic content to render
        self.page.wait_for_timeout(2000)

    def Maps_to_parts(self):
        """
        Click the main sidebar navigation link for 'Parts'.

        This method navigates to the Parts module by clicking the navigation menu.
        Uses multiple fallback strategies to handle different UI states.
        """
        # Try primary selector first
        try:
            self.click_element(self.PARTS_NAV_LINK)
            # Wait for navigation
            self.wait_for_load_state("networkidle")
            return
        except Exception:
            pass

        # Try alternative selector
        try:
            self.click_element(self.PARTS_NAV_LINK_ALT)
            self.wait_for_load_state("networkidle")
            return
        except Exception:
            pass

        # Last resort: navigate directly to URL
        self.navigate_to_parts()

    def click_new_part(self):
        """
        Click the button to create a new part.

        This opens the part creation form/dialog.
        Tries multiple selector strategies.
        """
        # Wait for page to be ready
        self.wait_for_load_state("domcontentloaded")

        # Try primary selector
        try:
            self.click_element(self.NEW_PART_BUTTON)
            # Wait for form to appear
            self.page.wait_for_timeout(1000)
            return
        except Exception:
            pass

        # Try alternative selector
        try:
            self.click_element(self.NEW_PART_BUTTON_ALT)
            self.page.wait_for_timeout(1000)
            return
        except Exception:
            raise Exception("Could not find 'New Part' button with any known selector")

    def fill_part_details(self, part_name: str, part_description: str):
        """
        Fill in the part creation form with name and description, then submit.

        This method:
        1. Fills the part name field
        2. Fills the part description field
        3. Clicks the submit/save button

        Args:
            part_name (str): Name for the new part
            part_description (str): Description for the new part

        Example:
            parts_page = PartsPage(page)
            parts_page.navigate_to_parts()
            parts_page.click_new_part()
            parts_page.fill_part_details("Resistor 10K", "10K Ohm resistor")
        """
        # Wait for form to be visible
        self.page.wait_for_timeout(1000)

        # Fill part name
        try:
            self.enter_text(self.PART_NAME_INPUT, part_name)
        except Exception:
            # Try alternative selector
            self.enter_text(self.PART_NAME_INPUT_ALT, part_name)

        # Small delay between fields
        self.page.wait_for_timeout(500)

        # Fill part description
        try:
            self.enter_text(self.PART_DESCRIPTION_INPUT, part_description)
        except Exception:
            # Try alternative selector
            self.enter_text(self.PART_DESCRIPTION_INPUT_ALT, part_description)

        # Small delay before submit
        self.page.wait_for_timeout(500)

        # Click submit button
        try:
            self.click_element(self.SUBMIT_BUTTON)
        except Exception:
            # Try alternative submit button selector
            self.click_element(self.SUBMIT_BUTTON_ALT)

        # Wait for form submission to complete
        self.wait_for_load_state("networkidle")

    def is_parts_page_loaded(self) -> bool:
        """
        Check if the Parts page is loaded.

        Returns:
            bool: True if on Parts page, False otherwise
        """
        # Check URL
        current_url = self.get_current_url()
        if "part" in current_url.lower():
            return True

        # Check for parts table or list
        return self.is_visible(self.PARTS_TABLE, timeout=5000)

    def get_part_count(self) -> int:
        """
        Get the number of parts displayed in the current view.

        Returns:
            int: Number of part rows visible
        """
        return self.get_element_count(self.PART_ROW)

    def search_part(self, search_term: str):
        """
        Search for parts using the search box.

        Args:
            search_term (str): Term to search for
        """
        search_selectors = [
            "input[type='search']",
            "input[placeholder*='Search' i]",
            "input[aria-label*='Search' i]",
        ]

        for selector in search_selectors:
            try:
                self.enter_text(selector, search_term)
                # Press Enter to search
                self.press_key(selector, "Enter")
                self.wait_for_load_state("networkidle")
                return
            except Exception:
                continue

        raise Exception("Could not find search input with any known selector")

    def click_part_by_name(self, part_name: str):
        """
        Click on a specific part by its name.

        Args:
            part_name (str): Name of the part to click
        """
        part_link = f"a:has-text('{part_name}'), td:has-text('{part_name}')"
        self.click_element(part_link)
        self.wait_for_load_state("networkidle")

    def is_new_part_form_visible(self) -> bool:
        """
        Check if the new part creation form is visible.

        Returns:
            bool: True if form is visible, False otherwise
        """
        try:
            name_visible = self.is_visible(self.PART_NAME_INPUT, timeout=3000)
            desc_visible = self.is_visible(self.PART_DESCRIPTION_INPUT, timeout=3000)
            return name_visible and desc_visible
        except:
            return False

    def cancel_part_creation(self):
        """
        Cancel the part creation process by clicking Cancel button.
        """
        self.click_element(self.CANCEL_BUTTON)
        self.page.wait_for_timeout(500)

    def verify_part_created(self, part_name: str) -> bool:
        """
        Verify that a part was created by checking if it appears in the list.

        Args:
            part_name (str): Name of the part to verify

        Returns:
            bool: True if part is found, False otherwise
        """
        # Wait for page to update
        self.page.wait_for_timeout(2000)

        # Check if part name appears on the page
        part_locator = f"text={part_name}"
        return self.is_visible(part_locator, timeout=5000)

    def fill_part_category(self, category_id: int):
        """
        Select a category for the part.

        Args:
            category_id (int): Category ID to select
        """
        self.select_dropdown_option(self.PART_CATEGORY_SELECT, str(category_id))

    def get_page_title(self) -> str:
        """
        Get the page title or heading.

        Returns:
            str: Page title text
        """
        title_selectors = ["h1", "h2", ".page-title", "[role='heading']"]

        for selector in title_selectors:
            try:
                return self.get_text(selector)
            except:
                continue

        return super().get_page_title()

    def wait_for_parts_table(self, timeout: int = 10000):
        """
        Wait for the parts table to load.

        Args:
            timeout (int): Maximum wait time in milliseconds
        """
        self.wait_for_selector(self.PARTS_TABLE, timeout=timeout)

    def take_parts_page_screenshot(self, path: str = "automation/ui/parts_page.png"):
        """
        Take a screenshot of the parts page.

        Args:
            path (str): File path for screenshot
        """
        self.take_screenshot(path)

    def Maps_to_stock_tab(self):
        """
        Click the Stock tab on a part's detail page.

        This method navigates to the stock view of the currently displayed part.
        Uses multiple fallback strategies to handle different UI states.

        Example:
            parts_page = PartsPage(page)
            parts_page.click_part_by_name("Test_Part_20240101")
            parts_page.Maps_to_stock_tab()
        """
        # Wait for page to be ready
        self.wait_for_load_state("domcontentloaded")

        # Try primary selector
        try:
            self.click_element(self.STOCK_TAB)
            # Wait for stock tab content to load
            self.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(1000)
            return
        except Exception:
            pass

        # Try alternative selector
        try:
            self.click_element(self.STOCK_TAB_ALT)
            self.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(1000)
            return
        except Exception:
            raise Exception("Could not find 'Stock' tab with any known selector")

    def click_add_stock(self):
        """
        Click the button to add new stock to a part.

        This opens the stock creation form/dialog.
        Tries multiple selector strategies.

        Example:
            parts_page = PartsPage(page)
            parts_page.Maps_to_stock_tab()
            parts_page.click_add_stock()
        """
        # Wait for page to be ready
        self.wait_for_load_state("domcontentloaded")

        # Try primary selector
        try:
            self.click_element(self.ADD_STOCK_BUTTON)
            # Wait for form to appear
            self.page.wait_for_timeout(1000)
            return
        except Exception:
            pass

        # Try alternative selector
        try:
            self.click_element(self.ADD_STOCK_BUTTON_ALT)
            self.page.wait_for_timeout(1000)
            return
        except Exception:
            raise Exception("Could not find 'Add Stock' button with any known selector")

    def fill_stock_details(self, quantity: int):
        """
        Fill in the stock creation form with quantity and submit.

        This method:
        1. Fills the quantity field
        2. Clicks the submit/save button

        Args:
            quantity (int): Quantity of stock items to add

        Example:
            parts_page = PartsPage(page)
            parts_page.click_add_stock()
            parts_page.fill_stock_details(100)
        """
        # Wait for form to be visible
        self.page.wait_for_timeout(1000)

        # Fill quantity
        try:
            self.enter_text(self.STOCK_QUANTITY_INPUT, str(quantity))
        except Exception:
            # Try alternative selector
            self.enter_text(self.STOCK_QUANTITY_INPUT_ALT, str(quantity))

        # Small delay before submit
        self.page.wait_for_timeout(500)

        # Click submit button (reuse existing locator)
        try:
            self.click_element(self.SUBMIT_BUTTON)
        except Exception:
            # Try alternative submit button selector
            self.click_element(self.SUBMIT_BUTTON_ALT)

        # Wait for form submission to complete
        self.wait_for_load_state("networkidle")
