"""
Playwright script to inspect InvenTree demo login page and identify correct selectors.

This script navigates to the actual login page and extracts selector information
for username, password, and login button elements.
"""
from playwright.sync_api import sync_playwright
import time


def inspect_login_page():
    """
    Inspect the InvenTree demo login page to find correct selectors.
    """
    with sync_playwright() as p:
        # Launch browser in headed mode so we can see what's happening
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context()
        page = context.new_page()

        print("=" * 80)
        print("InvenTree Demo Login Page Inspector")
        print("=" * 80)

        # Navigate to the login page
        print("\n1. Navigating to InvenTree demo...")
        try:
            page.goto("https://demo.inventree.org", wait_until="networkidle")
            print(f"   Current URL: {page.url}")
        except Exception as e:
            print(f"   Error navigating: {e}")
            browser.close()
            return

        # Wait a bit for page to fully load
        time.sleep(2)

        print("\n2. Page Information:")
        print(f"   Title: {page.title()}")
        print(f"   URL: {page.url}")

        # Take screenshot
        screenshot_path = "automation/ui/login_page_screenshot.png"
        page.screenshot(path=screenshot_path)
        print(f"   Screenshot saved: {screenshot_path}")

        print("\n3. Searching for login form elements...")

        # Common selectors to try for username
        username_selectors = [
            "input[name='username']",
            "input[id='username']",
            "input[type='text']",
            "input[placeholder*='username' i]",
            "input[placeholder*='user' i]",
            "input[autocomplete='username']",
            "#id_username",
            "[data-testid='username']",
            ".username-input",
        ]

        # Common selectors to try for password
        password_selectors = [
            "input[name='password']",
            "input[id='password']",
            "input[type='password']",
            "input[placeholder*='password' i]",
            "#id_password",
            "[data-testid='password']",
            ".password-input",
        ]

        # Common selectors for login button
        button_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button:has-text('Login')",
            "button:has-text('Sign in')",
            "button:has-text('Log in')",
            "[data-testid='login-button']",
            ".login-button",
            "#login-button",
        ]

        print("\n   Testing Username Field Selectors:")
        found_username = None
        for selector in username_selectors:
            try:
                element = page.locator(selector).first
                if element.count() > 0:
                    is_visible = element.is_visible(timeout=1000)
                    if is_visible:
                        attrs = {
                            "name": element.get_attribute("name"),
                            "id": element.get_attribute("id"),
                            "type": element.get_attribute("type"),
                            "placeholder": element.get_attribute("placeholder"),
                            "class": element.get_attribute("class"),
                        }
                        print(f"   ✅ FOUND: {selector}")
                        print(f"      Attributes: {attrs}")
                        if not found_username:
                            found_username = selector
            except Exception as e:
                pass

        print("\n   Testing Password Field Selectors:")
        found_password = None
        for selector in password_selectors:
            try:
                element = page.locator(selector).first
                if element.count() > 0:
                    is_visible = element.is_visible(timeout=1000)
                    if is_visible:
                        attrs = {
                            "name": element.get_attribute("name"),
                            "id": element.get_attribute("id"),
                            "type": element.get_attribute("type"),
                            "placeholder": element.get_attribute("placeholder"),
                            "class": element.get_attribute("class"),
                        }
                        print(f"   ✅ FOUND: {selector}")
                        print(f"      Attributes: {attrs}")
                        if not found_password:
                            found_password = selector
            except Exception as e:
                pass

        print("\n   Testing Login Button Selectors:")
        found_button = None
        for selector in button_selectors:
            try:
                element = page.locator(selector).first
                if element.count() > 0:
                    is_visible = element.is_visible(timeout=1000)
                    if is_visible:
                        attrs = {
                            "type": element.get_attribute("type"),
                            "class": element.get_attribute("class"),
                            "text": element.text_content()[:50],
                        }
                        print(f"   ✅ FOUND: {selector}")
                        print(f"      Attributes: {attrs}")
                        if not found_button:
                            found_button = selector
            except Exception as e:
                pass

        # Print all input fields on the page
        print("\n4. All Input Fields on Page:")
        try:
            all_inputs = page.locator("input").all()
            for i, input_elem in enumerate(all_inputs[:10]):  # Limit to first 10
                try:
                    if input_elem.is_visible(timeout=500):
                        print(f"   Input {i+1}:")
                        print(f"      Type: {input_elem.get_attribute('type')}")
                        print(f"      Name: {input_elem.get_attribute('name')}")
                        print(f"      ID: {input_elem.get_attribute('id')}")
                        print(f"      Placeholder: {input_elem.get_attribute('placeholder')}")
                except:
                    pass
        except Exception as e:
            print(f"   Error listing inputs: {e}")

        # Print all buttons on the page
        print("\n5. All Buttons on Page:")
        try:
            all_buttons = page.locator("button").all()
            for i, button_elem in enumerate(all_buttons[:10]):  # Limit to first 10
                try:
                    if button_elem.is_visible(timeout=500):
                        print(f"   Button {i+1}:")
                        print(f"      Type: {button_elem.get_attribute('type')}")
                        print(f"      Text: {button_elem.text_content()[:50]}")
                        print(f"      Class: {button_elem.get_attribute('class')}")
                except:
                    pass
        except Exception as e:
            print(f"   Error listing buttons: {e}")

        # Summary
        print("\n" + "=" * 80)
        print("RECOMMENDED SELECTORS:")
        print("=" * 80)
        if found_username:
            print(f"USERNAME_INPUT = \"{found_username}\"")
        else:
            print("USERNAME_INPUT = NOT FOUND - Check manual inspection")

        if found_password:
            print(f"PASSWORD_INPUT = \"{found_password}\"")
        else:
            print("PASSWORD_INPUT = NOT FOUND - Check manual inspection")

        if found_button:
            print(f"LOGIN_BUTTON = \"{found_button}\"")
        else:
            print("LOGIN_BUTTON = NOT FOUND - Check manual inspection")

        print(f"\nLOGIN_URL = \"{page.url}\"")
        print("=" * 80)

        # Keep browser open for manual inspection
        print("\n⏸️  Browser will stay open for 30 seconds for manual inspection...")
        print("   Use this time to inspect the page in DevTools if needed.")
        time.sleep(30)

        # Close browser
        browser.close()
        print("\n✅ Inspection complete!")


if __name__ == "__main__":
    inspect_login_page()
