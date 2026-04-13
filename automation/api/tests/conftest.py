"""
Pytest configuration and fixtures for InvenTree API tests.
"""
import pytest


@pytest.fixture(scope="session")
def base_url():
    """
    Provides the base URL for InvenTree API endpoint.

    Using the official InvenTree demo environment for testing.
    This allows testing against a live instance without local setup.

    Returns:
        str: Base API URL for InvenTree demo instance
    """
    return "https://demo.inventree.org/api/"


@pytest.fixture(scope="session")
def auth_headers():
    """
    Provides standard authentication headers for API requests.

    Note: Update with actual credentials or use environment variables
    for security in production environments.

    Returns:
        dict: Authentication headers
    """
    # For token-based authentication (InvenTree default)
    return {
        "Authorization": "Token YOUR_AUTH_TOKEN_HERE",
        "Content-Type": "application/json"
    }


@pytest.fixture(scope="session")
def basic_auth():
    """
    Provides basic authentication tuple for requests.

    Returns:
        tuple: (username, password) for basic auth
    """
    return ("admin", "admin")
