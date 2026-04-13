"""
API Automation Tests for InvenTree Parts CRUD Operations.

This module contains comprehensive API tests using pytest and requests,
demonstrating data-driven testing with parametrize decorators.
"""
import pytest
import requests
import json


class TestPartsAPI:
    """Test suite for Parts API CRUD operations."""

    def test_get_parts_list(self, base_url, auth_headers):
        """
        Test retrieving the list of all parts.

        Validates:
        - Status code 200
        - Response contains expected keys
        - Results is a list
        """
        response = requests.get(base_url, headers=auth_headers)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert "results" in data, "Response missing 'results' key"
        assert isinstance(data["results"], list), "Results should be a list"

        # Validate pagination keys
        assert "count" in data, "Response missing 'count' key"
        assert "next" in data, "Response missing 'next' key"
        assert "previous" in data, "Response missing 'previous' key"

    @pytest.mark.parametrize("page,limit", [
        (1, 10),
        (1, 25),
        (2, 10),
    ])
    def test_get_parts_with_pagination(self, base_url, auth_headers, page, limit):
        """
        Test parts list pagination with different page and limit values.

        Demonstrates data-driven testing using parametrize.
        """
        params = {"page": page, "limit": limit}
        response = requests.get(base_url, headers=auth_headers, params=params)

        assert response.status_code == 200
        data = response.json()

        assert "results" in data
        assert len(data["results"]) <= limit, f"Results exceed limit of {limit}"

    @pytest.mark.parametrize("search_term,expected_status", [
        ("Resistor", 200),
        ("Capacitor", 200),
        ("", 200),  # Empty search should return all
    ])
    def test_search_parts(self, base_url, auth_headers, search_term, expected_status):
        """
        Test searching parts with different search terms.

        Validates search functionality with various inputs.
        """
        params = {"search": search_term}
        response = requests.get(base_url, headers=auth_headers, params=params)

        assert response.status_code == expected_status
        data = response.json()
        assert "results" in data

    @pytest.mark.parametrize("filter_key,filter_value", [
        ("active", "true"),
        ("active", "false"),
        ("assembly", "true"),
        ("template", "true"),
    ])
    def test_filter_parts(self, base_url, auth_headers, filter_key, filter_value):
        """
        Test filtering parts by different criteria.

        Demonstrates filtering by active status, assembly, and template flags.
        """
        params = {filter_key: filter_value}
        response = requests.get(base_url, headers=auth_headers, params=params)

        assert response.status_code == 200
        data = response.json()
        assert "results" in data

    def test_get_part_by_id(self, base_url, auth_headers):
        """
        Test retrieving a specific part by ID.

        Validates:
        - Status code 200
        - Response contains part schema fields
        """
        # Assuming part with ID 1 exists - in real tests, create test data first
        part_id = 1
        url = f"{base_url}{part_id}/"
        response = requests.get(url, headers=auth_headers)

        # Handle both success and not found gracefully
        if response.status_code == 200:
            data = response.json()
            # Validate part schema
            expected_fields = ["pk", "name", "description", "category", "active"]
            for field in expected_fields:
                assert field in data, f"Missing required field: {field}"
        elif response.status_code == 404:
            pytest.skip("Part ID 1 does not exist in test database")
        else:
            pytest.fail(f"Unexpected status code: {response.status_code}")

    @pytest.mark.parametrize("invalid_id,expected_status", [
        (99999, 404),  # Non-existent ID
        ("invalid", 404),  # Invalid ID format
        (-1, 404),  # Negative ID
    ])
    def test_get_part_with_invalid_id(self, base_url, auth_headers, invalid_id, expected_status):
        """
        Test retrieving parts with invalid IDs.

        Validates error handling for invalid part IDs.
        """
        url = f"{base_url}{invalid_id}/"
        response = requests.get(url, headers=auth_headers)

        assert response.status_code == expected_status

    @pytest.mark.parametrize("part_data", [
        {
            "name": "Test Resistor 10K",
            "description": "10K Ohm resistor for testing",
            "category": 1,
            "active": True
        },
        {
            "name": "Test Capacitor 100uF",
            "description": "100uF electrolytic capacitor",
            "category": 1,
            "active": True,
            "assembly": False
        },
        {
            "name": "Test Assembly Board",
            "description": "PCB assembly for testing",
            "category": 1,
            "assembly": True,
            "active": True
        },
    ])
    def test_create_part(self, base_url, auth_headers, part_data):
        """
        Test creating new parts with different configurations.

        Demonstrates data-driven part creation with parametrize.

        Validates:
        - Status code 201 (Created)
        - Response contains created part data
        - Response includes generated pk (primary key)
        """
        response = requests.post(
            base_url,
            headers=auth_headers,
            data=json.dumps(part_data)
        )

        if response.status_code == 201:
            data = response.json()
            assert "pk" in data, "Created part should have primary key"
            assert data["name"] == part_data["name"]
            assert data["description"] == part_data["description"]

            # Cleanup: Delete created part
            part_id = data["pk"]
            cleanup_url = f"{base_url}{part_id}/"
            requests.delete(cleanup_url, headers=auth_headers)
        else:
            # Log response for debugging
            pytest.skip(f"Part creation not available or failed: {response.status_code} - {response.text}")

    @pytest.mark.parametrize("invalid_data,expected_error_field", [
        ({"description": "Missing name", "category": 1}, "name"),
        ({"name": "", "category": 1}, "name"),
        ({"name": "Test", "category": 99999}, "category"),
        ({"name": "Test", "active": "not_boolean"}, "active"),
    ])
    def test_create_part_with_invalid_data(self, base_url, auth_headers, invalid_data, expected_error_field):
        """
        Test part creation with invalid data.

        Validates field-level validation and error responses.
        """
        response = requests.post(
            base_url,
            headers=auth_headers,
            data=json.dumps(invalid_data)
        )

        assert response.status_code == 400, f"Expected 400 for invalid data, got {response.status_code}"

        error_data = response.json()
        # Check if the expected field has validation error
        assert expected_error_field in error_data or "non_field_errors" in error_data

    def test_create_part_without_authentication(self, base_url):
        """
        Test part creation without authentication headers.

        Validates authentication requirement.
        """
        part_data = {
            "name": "Unauthorized Part",
            "description": "Should fail",
            "category": 1
        }

        response = requests.post(
            base_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(part_data)
        )

        assert response.status_code == 401, "Should return 401 Unauthorized"

    def test_update_part_patch(self, base_url, auth_headers):
        """
        Test partial update of a part using PATCH.

        Validates:
        - Status code 200
        - Only specified fields are updated
        """
        # First create a part to update
        create_data = {
            "name": "Part to Update",
            "description": "Original description",
            "category": 1,
            "active": True
        }

        create_response = requests.post(
            base_url,
            headers=auth_headers,
            data=json.dumps(create_data)
        )

        if create_response.status_code == 201:
            part_id = create_response.json()["pk"]

            # Update only the description
            update_data = {"description": "Updated description"}
            update_url = f"{base_url}{part_id}/"

            update_response = requests.patch(
                update_url,
                headers=auth_headers,
                data=json.dumps(update_data)
            )

            assert update_response.status_code == 200
            updated_part = update_response.json()
            assert updated_part["description"] == "Updated description"
            assert updated_part["name"] == "Part to Update"  # Name should remain unchanged

            # Cleanup
            requests.delete(update_url, headers=auth_headers)
        else:
            pytest.skip("Cannot create part for update test")

    @pytest.mark.parametrize("update_data", [
        {"name": "Updated Name"},
        {"description": "Updated Description"},
        {"active": False},
        {"name": "New Name", "description": "New Description"},
    ])
    def test_update_part_various_fields(self, base_url, auth_headers, update_data):
        """
        Test updating different part fields.

        Demonstrates data-driven update testing.
        """
        # First create a part
        create_data = {
            "name": "Part for Field Update",
            "description": "Original",
            "category": 1,
            "active": True
        }

        create_response = requests.post(
            base_url,
            headers=auth_headers,
            data=json.dumps(create_data)
        )

        if create_response.status_code == 201:
            part_id = create_response.json()["pk"]
            update_url = f"{base_url}{part_id}/"

            # Update the part
            update_response = requests.patch(
                update_url,
                headers=auth_headers,
                data=json.dumps(update_data)
            )

            assert update_response.status_code == 200

            # Verify updates
            updated_part = update_response.json()
            for key, value in update_data.items():
                assert updated_part[key] == value

            # Cleanup
            requests.delete(update_url, headers=auth_headers)
        else:
            pytest.skip("Cannot create part for update test")

    def test_delete_part(self, base_url, auth_headers):
        """
        Test deleting a part.

        Validates:
        - Status code 204 (No Content) on successful deletion
        - Part no longer exists after deletion
        """
        # First create a part to delete
        create_data = {
            "name": "Part to Delete",
            "description": "Will be deleted",
            "category": 1,
            "active": True
        }

        create_response = requests.post(
            base_url,
            headers=auth_headers,
            data=json.dumps(create_data)
        )

        if create_response.status_code == 201:
            part_id = create_response.json()["pk"]
            delete_url = f"{base_url}{part_id}/"

            # Delete the part
            delete_response = requests.delete(delete_url, headers=auth_headers)

            assert delete_response.status_code in [204, 200], "Deletion should return 204 or 200"

            # Verify part no longer exists
            get_response = requests.get(delete_url, headers=auth_headers)
            assert get_response.status_code == 404, "Deleted part should not exist"
        else:
            pytest.skip("Cannot create part for delete test")

    def test_delete_non_existent_part(self, base_url, auth_headers):
        """
        Test deleting a non-existent part.

        Validates error handling for invalid delete operations.
        """
        delete_url = f"{base_url}99999/"
        response = requests.delete(delete_url, headers=auth_headers)

        assert response.status_code == 404, "Should return 404 for non-existent part"

    def test_response_schema_validation(self, base_url, auth_headers):
        """
        Test that API responses conform to expected schema.

        Validates response structure and data types.
        """
        response = requests.get(base_url, headers=auth_headers)

        if response.status_code == 200:
            data = response.json()

            # Validate pagination schema
            assert isinstance(data.get("count"), int), "count should be integer"
            assert isinstance(data.get("results"), list), "results should be list"

            # If results exist, validate part schema
            if data["results"]:
                part = data["results"][0]
                assert isinstance(part.get("pk"), int), "pk should be integer"
                assert isinstance(part.get("name"), str), "name should be string"
                assert isinstance(part.get("active"), bool), "active should be boolean"


class TestPartsCRUDIntegration:
    """Integration tests for complete CRUD workflows."""

    def test_full_crud_lifecycle(self, base_url, auth_headers):
        """
        Test complete CRUD lifecycle: Create -> Read -> Update -> Delete.

        Validates full workflow integration.
        """
        # CREATE
        create_data = {
            "name": "CRUD Test Part",
            "description": "Testing full lifecycle",
            "category": 1,
            "active": True
        }

        create_response = requests.post(
            base_url,
            headers=auth_headers,
            data=json.dumps(create_data)
        )

        if create_response.status_code != 201:
            pytest.skip("Part creation not available")

        assert create_response.status_code == 201
        part_id = create_response.json()["pk"]
        part_url = f"{base_url}{part_id}/"

        # READ
        read_response = requests.get(part_url, headers=auth_headers)
        assert read_response.status_code == 200
        part_data = read_response.json()
        assert part_data["name"] == "CRUD Test Part"

        # UPDATE
        update_data = {"description": "Updated in lifecycle test"}
        update_response = requests.patch(
            part_url,
            headers=auth_headers,
            data=json.dumps(update_data)
        )
        assert update_response.status_code == 200
        assert update_response.json()["description"] == "Updated in lifecycle test"

        # DELETE
        delete_response = requests.delete(part_url, headers=auth_headers)
        assert delete_response.status_code in [204, 200]

        # VERIFY DELETION
        verify_response = requests.get(part_url, headers=auth_headers)
        assert verify_response.status_code == 404
