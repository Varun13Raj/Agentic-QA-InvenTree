# InvenTree Parts Module - Manual API Test Cases

## Test Suite Overview
Comprehensive manual API test cases for InvenTree Parts module covering all CRUD operations, authentication, validation, filtering, pagination, and error handling.

## API Base Information
- **Base URL**: `http://localhost:8000/api/` or `https://<inventree-instance>/api/`
- **Authentication**: Token-based authentication
- **Content-Type**: `application/json`
- **API Version**: Check via `/api/` endpoint

---

## Test Cases

| Test ID | Module | Endpoint | HTTP Method | Scenario Description | Request Details | Expected Response | Status Code | Test Type |
|---------|--------|----------|-------------|---------------------|-----------------|-------------------|-------------|-----------|
| TC-API-001 | Authentication | `/api/user/token/` | POST | Obtain authentication token with valid credentials | **Body:**<br>`{"username": "testuser", "password": "validpass"}` | Token returned in response:<br>`{"token": "abc123xyz..."}` | 200 | Positive |
| TC-API-002 | Authentication | `/api/user/token/` | POST | Attempt authentication with invalid credentials | **Body:**<br>`{"username": "testuser", "password": "wrongpass"}` | Error message:<br>`{"non_field_errors": ["Unable to log in..."]}` | 400/401 | Negative |
| TC-API-003 | Authentication | `/api/user/token/` | POST | Attempt authentication without credentials | **Body:**<br>`{}` | Validation errors for required fields | 400 | Negative |
| TC-API-004 | Authentication | `/api/part/` | GET | Access protected endpoint without token | **Headers:**<br>No Authorization header | Error: Authentication credentials not provided | 401 | Negative |
| TC-API-005 | Authentication | `/api/part/` | GET | Access protected endpoint with invalid token | **Headers:**<br>`Authorization: Token invalidtoken123` | Error: Invalid token | 401 | Negative |
| TC-API-006 | Parts List | `/api/part/` | GET | Retrieve all parts | **Headers:**<br>`Authorization: Token <valid_token>` | Array of part objects with pagination info | 200 | Positive |
| TC-API-007 | Parts List | `/api/part/` | GET | Retrieve parts with pagination (page 1) | **Query Params:**<br>`?page=1&limit=10` | First 10 parts with pagination metadata | 200 | Positive |
| TC-API-008 | Parts List | `/api/part/` | GET | Retrieve parts with pagination (specific page) | **Query Params:**<br>`?page=2&limit=10` | Parts 11-20 with pagination metadata | 200 | Positive |
| TC-API-009 | Parts List | `/api/part/` | GET | Retrieve parts with invalid page number | **Query Params:**<br>`?page=-1` | Empty results or error message | 400/200 | Boundary |
| TC-API-010 | Parts List | `/api/part/` | GET | Retrieve parts with excessive page number | **Query Params:**<br>`?page=99999` | Empty results with valid pagination structure | 200 | Boundary |
| TC-API-011 | Parts Search | `/api/part/` | GET | Search parts by name | **Query Params:**<br>`?search=Resistor` | Parts matching "Resistor" in name/description | 200 | Positive |
| TC-API-012 | Parts Search | `/api/part/` | GET | Search parts with special characters | **Query Params:**<br>`?search=@#$%` | Empty results or matching parts, no error | 200 | Boundary |
| TC-API-013 | Parts Search | `/api/part/` | GET | Search parts with empty search term | **Query Params:**<br>`?search=` | All parts returned (or error based on API design) | 200 | Boundary |
| TC-API-014 | Parts Filter | `/api/part/` | GET | Filter parts by category | **Query Params:**<br>`?category=5` | Parts in category ID 5 only | 200 | Positive |
| TC-API-015 | Parts Filter | `/api/part/` | GET | Filter parts by active status | **Query Params:**<br>`?active=true` | Only active parts returned | 200 | Positive |
| TC-API-016 | Parts Filter | `/api/part/` | GET | Filter parts by assembly flag | **Query Params:**<br>`?assembly=true` | Only assembly parts returned | 200 | Positive |
| TC-API-017 | Parts Filter | `/api/part/` | GET | Filter parts by template flag | **Query Params:**<br>`?template=true` | Only template parts returned | 200 | Positive |
| TC-API-018 | Parts Filter | `/api/part/` | GET | Filter parts with multiple criteria | **Query Params:**<br>`?category=5&active=true&assembly=true` | Parts matching all filter criteria | 200 | Positive |
| TC-API-019 | Parts Filter | `/api/part/` | GET | Filter parts by non-existent category | **Query Params:**<br>`?category=99999` | Empty results array | 200 | Negative |
| TC-API-020 | Parts Filter | `/api/part/` | GET | Filter parts with invalid parameter type | **Query Params:**<br>`?active=invalid` | Validation error or default behavior | 400/200 | Negative |
| TC-API-021 | Parts Detail | `/api/part/{id}/` | GET | Retrieve specific part by valid ID | **Path Param:**<br>`id=1` | Complete part object with all fields | 200 | Positive |
| TC-API-022 | Parts Detail | `/api/part/{id}/` | GET | Retrieve part with non-existent ID | **Path Param:**<br>`id=99999` | Error: Not found | 404 | Negative |
| TC-API-023 | Parts Detail | `/api/part/{id}/` | GET | Retrieve part with invalid ID format | **Path Param:**<br>`id=abc` | Error: Invalid ID format | 400/404 | Negative |
| TC-API-024 | Parts Detail | `/api/part/{id}/` | GET | Retrieve part with negative ID | **Path Param:**<br>`id=-1` | Error: Invalid ID or Not found | 400/404 | Boundary |
| TC-API-025 | Parts Create | `/api/part/` | POST | Create new part with all required fields | **Body:**<br>`{"name": "New Part", "description": "Test part", "category": 1, "active": true}` | Part created, returns created object with ID | 201 | Positive |
| TC-API-026 | Parts Create | `/api/part/` | POST | Create new part with all fields | **Body:**<br>`{"name": "Complete Part", "description": "Full test", "category": 1, "IPN": "IPN-001", "active": true, "assembly": false, "template": false, "keywords": "test"}` | Part created with all fields populated | 201 | Positive |
| TC-API-027 | Parts Create | `/api/part/` | POST | Create part without required name field | **Body:**<br>`{"description": "Test", "category": 1}` | Validation error: name is required | 400 | Negative |
| TC-API-028 | Parts Create | `/api/part/` | POST | Create part without required category | **Body:**<br>`{"name": "Test Part", "description": "Test"}` | Part created with null/default category OR validation error | 201/400 | Negative |
| TC-API-029 | Parts Create | `/api/part/` | POST | Create part with empty name | **Body:**<br>`{"name": "", "description": "Test", "category": 1}` | Validation error: name cannot be empty | 400 | Negative |
| TC-API-030 | Parts Create | `/api/part/` | POST | Create part with duplicate IPN | **Body:**<br>`{"name": "Part 2", "IPN": "EXISTING-IPN", "category": 1}` | Validation error: IPN must be unique | 400 | Negative |
| TC-API-031 | Parts Create | `/api/part/` | POST | Create part with name at max length | **Body:**<br>`{"name": "<255 chars>", "category": 1}` | Part created successfully | 201 | Boundary |
| TC-API-032 | Parts Create | `/api/part/` | POST | Create part with name exceeding max length | **Body:**<br>`{"name": "<256+ chars>", "category": 1}` | Validation error: name too long | 400 | Boundary |
| TC-API-033 | Parts Create | `/api/part/` | POST | Create part with special characters | **Body:**<br>`{"name": "Part@#$%&*", "category": 1}` | Part created with special characters | 201 | Boundary |
| TC-API-034 | Parts Create | `/api/part/` | POST | Create part with invalid category ID | **Body:**<br>`{"name": "Test", "category": 99999}` | Validation error: invalid category | 400 | Negative |
| TC-API-035 | Parts Create | `/api/part/` | POST | Create part with invalid data type | **Body:**<br>`{"name": "Test", "category": "string", "active": "not_boolean"}` | Validation error: invalid data types | 400 | Negative |
| TC-API-036 | Parts Create | `/api/part/` | POST | Create assembly part | **Body:**<br>`{"name": "Assembly", "category": 1, "assembly": true}` | Assembly part created with assembly flag true | 201 | Positive |
| TC-API-037 | Parts Create | `/api/part/` | POST | Create template part | **Body:**<br>`{"name": "Template", "category": 1, "template": true}` | Template part created with template flag true | 201 | Positive |
| TC-API-038 | Parts Create | `/api/part/` | POST | Create part with null values for optional fields | **Body:**<br>`{"name": "Test", "category": 1, "IPN": null, "revision": null}` | Part created, null values accepted | 201 | Positive |
| TC-API-039 | Parts Create | `/api/part/` | POST | Create part with malformed JSON | **Body:**<br>`{name: "Test", category: 1}` (missing quotes) | Error: Invalid JSON format | 400 | Negative |
| TC-API-040 | Parts Create | `/api/part/` | POST | Create part with extra unexpected fields | **Body:**<br>`{"name": "Test", "category": 1, "unexpected_field": "value"}` | Part created, unexpected field ignored OR error | 201/400 | Boundary |
| TC-API-041 | Parts Update | `/api/part/{id}/` | PUT | Update entire part with valid data | **Body:**<br>`{"name": "Updated Part", "description": "Updated", "category": 1, "active": true}` | Part fully updated with new values | 200 | Positive |
| TC-API-042 | Parts Update | `/api/part/{id}/` | PUT | Update part without required fields | **Body:**<br>`{"description": "Updated"}` (missing name) | Validation error: required fields missing | 400 | Negative |
| TC-API-043 | Parts Update | `/api/part/{id}/` | PATCH | Partially update part name only | **Body:**<br>`{"name": "Patched Name"}` | Part name updated, other fields unchanged | 200 | Positive |
| TC-API-044 | Parts Update | `/api/part/{id}/` | PATCH | Partially update multiple fields | **Body:**<br>`{"name": "New Name", "description": "New Desc"}` | Specified fields updated, others unchanged | 200 | Positive |
| TC-API-045 | Parts Update | `/api/part/{id}/` | PATCH | Update part with invalid data | **Body:**<br>`{"active": "not_boolean"}` | Validation error: invalid data type | 400 | Negative |
| TC-API-046 | Parts Update | `/api/part/{id}/` | PATCH | Update non-existent part | **Path Param:** `id=99999`<br>**Body:** `{"name": "Test"}` | Error: Not found | 404 | Negative |
| TC-API-047 | Parts Update | `/api/part/{id}/` | PATCH | Update part with duplicate IPN | **Body:**<br>`{"IPN": "EXISTING-IPN"}` | Validation error: IPN must be unique | 400 | Negative |
| TC-API-048 | Parts Update | `/api/part/{id}/` | PATCH | Clear optional field with null | **Body:**<br>`{"IPN": null}` | Field cleared/set to null | 200 | Positive |
| TC-API-049 | Parts Update | `/api/part/{id}/` | PATCH | Update part to assembly type | **Body:**<br>`{"assembly": true}` | Part converted to assembly type | 200 | Positive |
| TC-API-050 | Parts Update | `/api/part/{id}/` | PATCH | Update part category | **Body:**<br>`{"category": 2}` | Part moved to new category | 200 | Positive |
| TC-API-051 | Parts Delete | `/api/part/{id}/` | DELETE | Delete part with no dependencies | **Path Param:**<br>`id=1` | Part deleted successfully | 204 | Positive |
| TC-API-052 | Parts Delete | `/api/part/{id}/` | DELETE | Delete non-existent part | **Path Param:**<br>`id=99999` | Error: Not found | 404 | Negative |
| TC-API-053 | Parts Delete | `/api/part/{id}/` | DELETE | Delete part with stock items | **Path Param:**<br>`id=<part_with_stock>` | Error: Cannot delete part with stock | 400 | Negative |
| TC-API-054 | Parts Delete | `/api/part/{id}/` | DELETE | Delete part used in BOM | **Path Param:**<br>`id=<part_in_bom>` | Error: Cannot delete part used in assemblies | 400 | Negative |
| TC-API-055 | Parts Delete | `/api/part/{id}/` | DELETE | Delete part with invalid ID format | **Path Param:**<br>`id=abc` | Error: Invalid ID format | 400/404 | Negative |
| TC-API-056 | Part Parameters | `/api/part/{id}/parameters/` | GET | Get all parameters for a part | **Path Param:**<br>`id=1` | Array of parameter objects | 200 | Positive |
| TC-API-057 | Part Parameters | `/api/part/{id}/parameters/` | GET | Get parameters for part with no parameters | **Path Param:**<br>`id=<no_params>` | Empty array | 200 | Positive |
| TC-API-058 | Part Parameters | `/api/part/parameter/` | POST | Add parameter to part | **Body:**<br>`{"part": 1, "template": 1, "data": "100"}` | Parameter created and linked to part | 201 | Positive |
| TC-API-059 | Part Parameters | `/api/part/parameter/` | POST | Add parameter with invalid template | **Body:**<br>`{"part": 1, "template": 99999, "data": "100"}` | Validation error: invalid template | 400 | Negative |
| TC-API-060 | Part Parameters | `/api/part/parameter/` | POST | Add duplicate parameter to part | **Body:**<br>`{"part": 1, "template": 1, "data": "100"}` (already exists) | Validation error: parameter exists OR allowed | 400/201 | Negative |
| TC-API-061 | Part Parameters | `/api/part/parameter/{id}/` | PATCH | Update parameter value | **Body:**<br>`{"data": "200"}` | Parameter value updated | 200 | Positive |
| TC-API-062 | Part Parameters | `/api/part/parameter/{id}/` | DELETE | Delete parameter from part | **Path Param:**<br>`id=1` | Parameter deleted | 204 | Positive |
| TC-API-063 | Part Stock | `/api/part/{id}/stock/` | GET | Get stock items for part | **Path Param:**<br>`id=1` | Array of stock items for the part | 200 | Positive |
| TC-API-064 | Part Stock | `/api/part/{id}/stock/` | GET | Get stock for part with no stock | **Path Param:**<br>`id=<no_stock>` | Empty array | 200 | Positive |
| TC-API-065 | Part BOM | `/api/bom/` | GET | Get BOM items for assembly part | **Query Params:**<br>`?part=1` | Array of BOM items | 200 | Positive |
| TC-API-066 | Part BOM | `/api/bom/` | POST | Add component to assembly BOM | **Body:**<br>`{"part": 1, "sub_part": 2, "quantity": 5}` | BOM item created | 201 | Positive |
| TC-API-067 | Part BOM | `/api/bom/` | POST | Add BOM item with invalid quantity | **Body:**<br>`{"part": 1, "sub_part": 2, "quantity": -1}` | Validation error: invalid quantity | 400 | Negative |
| TC-API-068 | Part BOM | `/api/bom/` | POST | Add BOM item to non-assembly part | **Body:**<br>`{"part": <non_assembly>, "sub_part": 2, "quantity": 1}` | Error: Cannot add BOM to non-assembly | 400 | Negative |
| TC-API-069 | Part BOM | `/api/bom/{id}/` | PATCH | Update BOM item quantity | **Body:**<br>`{"quantity": 10}` | BOM quantity updated | 200 | Positive |
| TC-API-070 | Part BOM | `/api/bom/{id}/` | DELETE | Remove component from BOM | **Path Param:**<br>`id=1` | BOM item deleted | 204 | Positive |
| TC-API-071 | Part Categories | `/api/part/category/` | GET | Get all part categories | - | Array of category objects in tree structure | 200 | Positive |
| TC-API-072 | Part Categories | `/api/part/category/` | POST | Create new category | **Body:**<br>`{"name": "New Category", "description": "Test"}` | Category created | 201 | Positive |
| TC-API-073 | Part Categories | `/api/part/category/` | POST | Create subcategory | **Body:**<br>`{"name": "Subcategory", "parent": 1}` | Subcategory created under parent | 201 | Positive |
| TC-API-074 | Part Categories | `/api/part/category/` | POST | Create category with duplicate name | **Body:**<br>`{"name": "Existing Category"}` | Category created OR error if duplicates not allowed | 201/400 | Negative |
| TC-API-075 | Part Categories | `/api/part/category/{id}/` | GET | Get specific category details | **Path Param:**<br>`id=1` | Category object with details | 200 | Positive |
| TC-API-076 | Part Categories | `/api/part/category/{id}/` | PATCH | Update category name | **Body:**<br>`{"name": "Updated Category"}` | Category updated | 200 | Positive |
| TC-API-077 | Part Categories | `/api/part/category/{id}/` | DELETE | Delete empty category | **Path Param:**<br>`id=<empty_category>` | Category deleted | 204 | Positive |
| TC-API-078 | Part Categories | `/api/part/category/{id}/` | DELETE | Delete category with parts | **Path Param:**<br>`id=<category_with_parts>` | Error: Cannot delete category with parts | 400 | Negative |
| TC-API-079 | Part Attachments | `/api/part/{id}/attachments/` | GET | Get all attachments for part | **Path Param:**<br>`id=1` | Array of attachment objects | 200 | Positive |
| TC-API-080 | Part Attachments | `/api/part/attachment/` | POST | Upload attachment to part | **Body (multipart):**<br>`part=1, attachment=<file>` | Attachment uploaded and linked | 201 | Positive |
| TC-API-081 | Part Attachments | `/api/part/attachment/` | POST | Upload invalid file type | **Body (multipart):**<br>`part=1, attachment=<.exe file>` | Error: Invalid file type | 400 | Negative |
| TC-API-082 | Part Attachments | `/api/part/attachment/` | POST | Upload oversized file | **Body (multipart):**<br>`part=1, attachment=<large file>` | Error: File size exceeds limit | 400 | Boundary |
| TC-API-083 | Part Attachments | `/api/part/attachment/{id}/` | DELETE | Delete attachment | **Path Param:**<br>`id=1` | Attachment deleted | 204 | Positive |
| TC-API-084 | Part Suppliers | `/api/company/part/` | GET | Get supplier parts for a part | **Query Params:**<br>`?part=1` | Array of supplier part objects | 200 | Positive |
| TC-API-085 | Part Suppliers | `/api/company/part/` | POST | Add supplier to part | **Body:**<br>`{"part": 1, "supplier": 1, "SKU": "SUP-001"}` | Supplier part created | 201 | Positive |
| TC-API-086 | Part Suppliers | `/api/company/part/` | POST | Add supplier with duplicate SKU | **Body:**<br>`{"part": 1, "supplier": 1, "SKU": "EXISTING-SKU"}` | Error: Duplicate SKU | 400 | Negative |
| TC-API-087 | Part Suppliers | `/api/company/part/{id}/` | PATCH | Update supplier SKU | **Body:**<br>`{"SKU": "NEW-SKU"}` | SKU updated | 200 | Positive |
| TC-API-088 | Part Suppliers | `/api/company/part/{id}/` | DELETE | Remove supplier from part | **Path Param:**<br>`id=1` | Supplier part deleted | 204 | Positive |
| TC-API-089 | Bulk Operations | `/api/part/` | GET | Retrieve parts with large page size | **Query Params:**<br>`?limit=1000` | Large batch of parts OR limited to max allowed | 200 | Boundary |
| TC-API-090 | Bulk Operations | `/api/part/` | GET | Retrieve parts with ordering | **Query Params:**<br>`?ordering=name` | Parts sorted by name ascending | 200 | Positive |
| TC-API-091 | Bulk Operations | `/api/part/` | GET | Retrieve parts with descending order | **Query Params:**<br>`?ordering=-name` | Parts sorted by name descending | 200 | Positive |
| TC-API-092 | Rate Limiting | `/api/part/` | GET | Make multiple rapid requests | Multiple rapid GET requests | Requests succeed OR rate limit response | 200/429 | Boundary |
| TC-API-093 | Content Type | `/api/part/` | POST | Create part with XML content type | **Headers:**<br>`Content-Type: application/xml` | Error: Unsupported content type OR XML parsed | 400/201 | Negative |
| TC-API-094 | Content Type | `/api/part/` | POST | Create part without content type header | No Content-Type header | Default to JSON OR error | 201/400 | Negative |
| TC-API-095 | CORS | `/api/part/` | OPTIONS | Check CORS preflight | OPTIONS request with Origin header | CORS headers in response | 200 | Positive |
| TC-API-096 | API Versioning | `/api/` | GET | Check API version info | - | API version and build info returned | 200 | Positive |
| TC-API-097 | Error Handling | `/api/invalid-endpoint/` | GET | Access non-existent endpoint | - | Error: Not found | 404 | Negative |
| TC-API-098 | Error Handling | `/api/part/` | POST | Send request with missing content type | **Body:** `{"name": "Test"}` No Content-Type | Error OR defaults to JSON | 400/201 | Negative |
| TC-API-099 | Concurrency | `/api/part/{id}/` | PATCH | Update same part simultaneously | Two PATCH requests at same time | Last write wins OR optimistic locking | 200/409 | Boundary |
| TC-API-100 | Response Format | `/api/part/` | GET | Request JSON response format | **Headers:**<br>`Accept: application/json` | JSON response returned | 200 | Positive |

---

## Test Execution Guidelines

### Prerequisites
1. **InvenTree Instance**: Running InvenTree server (localhost or remote)
2. **Test User Account**: User with appropriate permissions for CRUD operations
3. **API Client**: Postman, cURL, REST Client, or automated test framework
4. **Test Data**: Pre-created categories, parts, and related entities

### Authentication Setup
```bash
# Obtain token
curl -X POST http://localhost:8000/api/user/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'

# Use token in subsequent requests
curl -X GET http://localhost:8000/api/part/ \
  -H "Authorization: Token <your-token-here>"
```

### Test Data Preparation
- Create test categories before testing part creation
- Prepare test parts for update/delete operations
- Create parameter templates for parameter testing
- Set up suppliers/manufacturers for relationship testing

### Expected Response Structure
Most InvenTree API responses follow this pattern:
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/part/?page=2",
  "previous": null,
  "results": [
    {
      "pk": 1,
      "name": "Part Name",
      "description": "Description",
      "category": 1,
      "IPN": "IPN-001",
      "active": true,
      ...
    }
  ]
}
```

### Error Response Structure
```json
{
  "field_name": ["Error message"],
  "non_field_errors": ["General error message"]
}
```

### Testing Tools Recommendations
- **Postman**: For manual testing with collections
- **cURL**: For command-line testing
- **Python Requests**: For scripting and automation
- **Newman**: For CI/CD integration of Postman collections
- **REST Assured**: For Java-based API testing

### Test Reporting
Document for each test:
- Request URL, method, headers, body
- Response status code, headers, body
- Pass/Fail status
- Screenshots or logs for failures
- Execution timestamp

## Coverage Summary

- **Authentication**: 5 test cases
- **Parts List & Pagination**: 5 test cases
- **Parts Search**: 3 test cases
- **Parts Filter**: 7 test cases
- **Parts Detail**: 4 test cases
- **Parts Create**: 16 test cases
- **Parts Update**: 10 test cases
- **Parts Delete**: 5 test cases
- **Part Parameters**: 7 test cases
- **Part Stock**: 2 test cases
- **Part BOM**: 6 test cases
- **Part Categories**: 8 test cases
- **Part Attachments**: 5 test cases
- **Part Suppliers**: 4 test cases
- **Bulk Operations**: 3 test cases
- **Edge Cases & Error Handling**: 10 test cases

**Total**: 100 comprehensive API test cases

## Automation Considerations

These manual test cases can be automated using:
- **Python**: `requests` + `pytest`
- **JavaScript**: `axios` + `jest` or `mocha`
- **Postman**: Collection with Newman CLI
- **REST Assured**: Java framework for API testing

Example automation structure:
```
automation/api/
├── tests/
│   ├── test_auth.py
│   ├── test_parts_crud.py
│   ├── test_parts_search_filter.py
│   ├── test_parts_parameters.py
│   └── test_parts_relationships.py
├── fixtures/
│   └── test_data.json
├── utils/
│   └── api_client.py
└── requirements.txt
```
