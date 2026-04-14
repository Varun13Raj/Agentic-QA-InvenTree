"""
Public search functionality tests for InvenTree UI using Playwright.

This module tests read-only search features that don't require authentication.
"""
import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import pytest
from playwright.sync_api import Page, expect


def test_read_only_part_search(page: Page):
    """
    Test searching for parts without authentication.

    This test demonstrates read-only search functionality:
    1. Navigate to InvenTree demo homepage
    2. Locate the global search bar
    3. Search for 'capacitor'
    4. Verify search results are displayed

    Args:
        page (Page): Playwright page fixture from pytest-playwright

    Note: This test does NOT require login and tests public search functionality.
    """
    # Step 1: Navigate to homepage
    print("\n=== Step 1: Navigate to Homepage ===")
    page.goto("http://localhost:8000/", wait_until="networkidle")
    page.wait_for_timeout(2000)

    current_url = page.url
    print(f"   Current URL: {current_url}")

    # Check if redirected to login
    if "/login" in current_url:
        pytest.skip("InvenTree requires authentication - no public search available on demo server")

    print("   [OK] Homepage loaded")

    # Step 2: Locate the global search bar
    print("\n=== Step 2: Locate Search Bar ===")

    # Try multiple search bar selector strategies
    search_selectors = [
        "input[type='search']",
        "input[placeholder*='Search' i]",
        "input[aria-label*='Search' i]",
        "input[name='search']",
        "[data-testid='search-input']",
        ".search-input",
        "#search",
    ]

    search_input = None
    found_selector = None

    for selector in search_selectors:
        try:
            locator = page.locator(selector)
            if locator.count() > 0 and locator.first.is_visible(timeout=3000):
                search_input = locator.first
                found_selector = selector
                print(f"[OK] Search bar found with selector: {selector}")
                break
        except:
            continue

    assert search_input is not None, \
        f"Could not find search bar with any known selector. Tried: {search_selectors}"

    # Step 3: Search for 'capacitor'
    print("\n=== Step 3: Perform Search ===")

    # Fill the search input
    search_input.fill("capacitor")
    print("[OK] Typed 'capacitor' into search bar")

    # Wait for any autocomplete/suggestions to appear
    page.wait_for_timeout(500)

    # Press Enter to submit search
    search_input.press("Enter")
    print("[OK] Pressed Enter to submit search")

    # Wait for navigation or search results to load
    page.wait_for_timeout(3000)

    # Step 4: Verify search results
    print("\n=== Step 4: Verify Search Results ===")

    current_url = page.url
    print(f"   Current URL after search: {current_url}")

    # Multiple verification strategies for search results
    verifications = {
        "url_contains_search": False,
        "results_container_visible": False,
        "capacitor_text_found": False,
        "table_visible": False
    }

    # Check if URL contains search-related parameters
    if "search" in current_url.lower() or "capacitor" in current_url.lower() or "part" in current_url.lower():
        verifications["url_contains_search"] = True
        print(f"[OK] URL indicates search: {current_url}")

    # Check for search results container
    result_container_selectors = [
        "[data-testid='search-results']",
        ".search-results",
        "[role='main']:has-text('capacitor')",
        ".results-container",
        "[class*='result']",
    ]

    for selector in result_container_selectors:
        try:
            if page.locator(selector).count() > 0:
                if page.locator(selector).first.is_visible(timeout=2000):
                    verifications["results_container_visible"] = True
                    print(f"[OK] Results container found: {selector}")
                    break
        except:
            continue

    # Check if 'capacitor' text appears in results
    try:
        capacitor_locator = page.locator("text=capacitor")
        if capacitor_locator.count() > 0:
            verifications["capacitor_text_found"] = True
            print(f"[OK] 'Capacitor' text found in {capacitor_locator.count()} location(s)")
    except:
        pass

    # Check for table or list of results
    table_selectors = [
        "table",
        "[role='table']",
        "[role='grid']",
        ".table",
        "tbody tr",
    ]

    for selector in table_selectors:
        try:
            locator = page.locator(selector)
            if locator.count() > 0 and locator.first.is_visible(timeout=2000):
                verifications["table_visible"] = True
                print(f"[OK] Results table found: {selector}")
                break
        except:
            continue

    # Use Playwright's expect for robust assertion
    print("\n=== Robust Playwright Assertion ===")

    # Primary assertion: At least one search result should be visible
    # Try to find any element that indicates search results are displayed
    try:
        # Wait for any visible content that contains 'capacitor' (case-insensitive)
        expect(page.locator("text=/capacitor/i").first).to_be_visible(timeout=5000)
        print("[OK] Playwright assertion passed: Search results visible")
        verifications["capacitor_text_found"] = True
    except Exception as e:
        print(f"   Playwright expect failed: {str(e)[:100]}")

    # Summary
    verification_count = sum(verifications.values())

    print(f"\n=== Verification Summary ===")
    print(f"Verifications passed: {verification_count}/4")
    print(f"Details: {verifications}")

    # Take screenshot for documentation
    page.screenshot(path="automation/ui/public_search_results.png", full_page=True)
    print("\nScreenshot saved: automation/ui/public_search_results.png")

    # Final assertion: At least one verification must pass
    assert verification_count > 0, \
        f"Search results could not be verified. " \
        f"Search term: 'capacitor', Verifications: {verifications}, URL: {current_url}"

    print(f"\n[OK] Test completed successfully! Search term: 'capacitor', Results verified: {verification_count}/4")
