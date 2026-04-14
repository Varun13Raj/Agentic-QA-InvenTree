"""
Pytest configuration and fixtures for InvenTree API tests.
"""
import pytest


@pytest.fixture(scope="session")
def base_url():
    """
    Provides the base URL for InvenTree API endpoint.

    Using the local Docker InvenTree instance for testing.
    Ensure Docker container is running: docker compose up -d

    Returns:
        str: Base API URL for local InvenTree instance
    """
    return "http://localhost:8000/api/"


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

    Uses the default credentials for local Docker InvenTree instance.

    Returns:
        tuple: (username, password) for basic auth
    """
    return ("admin", "inventree")
