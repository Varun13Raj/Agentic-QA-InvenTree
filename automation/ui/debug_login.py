"""
Debug script to investigate InvenTree demo login behavior.
"""
from playwright.sync_api import sync_playwright
import time


def debug_login():
    """Debug the login process step by step."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to login page...")
        page.goto("https://demo.inventree.org/web/login", wait_until="networkidle")
        time.sleep(2)

        print(f"Current URL: {page.url}")
        print(f"Page title: {page.title()}")

        # Try to find and fill username
        username_input = page.locator("input[placeholder='Your username']")
        print(f"Username input count: {username_input.count()}")

        if username_input.count() > 0:
            print("Filling username...")
            username_input.fill("admin")
            time.sleep(1)

        # Try to find and fill password
        password_input = page.locator("input[type='password']")
        print(f"Password input count: {password_input.count()}")

        if password_input.count() > 0:
            print("Filling password...")
            password_input.fill("inventree")
            time.sleep(1)

        # Try to find login button
        login_button = page.locator("button[type='submit']:has-text('Log In')")
        print(f"Login button count: {login_button.count()}")

        if login_button.count() > 0:
            print("Clicking login button...")
            login_button.click()

            # Wait and see what happens
            print("Waiting for navigation...")
            time.sleep(5)

            print(f"After login URL: {page.url}")
            print(f"After login title: {page.title()}")

            # Check for error messages
            errors = page.locator("[role='alert']").all()
            if errors:
                print(f"Found {len(errors)} alert(s)")
                for error in errors:
                    if error.is_visible():
                        print(f"Error text: {error.text_content()}")

        # Take screenshot
        page.screenshot(path="automation/ui/debug_login_result.png")
        print("Screenshot saved: automation/ui/debug_login_result.png")

        # Keep open for manual inspection
        print("\nKeeping browser open for 20 seconds for manual inspection...")
        time.sleep(20)

        browser.close()


if __name__ == "__main__":
    debug_login()
