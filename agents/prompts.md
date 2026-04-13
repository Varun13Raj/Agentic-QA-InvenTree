# Agent Prompts

## UI Manual Test Case Generation for InvenTree Parts Module

Act as a Senior Quality Engineering Architect. I need you to ingest the InvenTree Parts documentation from https://docs.inventree.org/en/stable/part/ (including sub-pages like Part Views, Parameters, Templates, Revisions). Generate a comprehensive suite of manual UI test cases specifically for the Parts module covering creation, all detail view tabs, categories, and revisions, including negative and boundary scenarios. Output the test cases as a detailed Markdown table with columns: Test ID, Module, Scenario Description, Steps to Reproduce, Expected Result, Test Type (Positive/Negative/Boundary). Action: Save the final markdown table directly into the test-cases folder as ui-manual-tests.md. Also, save this exact prompt instruction into the agents folder as a file named prompts.md.

## API Manual Test Case Generation for InvenTree Parts Module

Act as a Senior API Test Architect. Based on the InvenTree API schema for the Parts module, generate a comprehensive suite of manual API test cases. Constraints: - Must cover: CRUD operations on Parts and Part Categories. - Must include: Filtering, pagination, and search on the Parts list endpoint. - Must test: Field-level validation (required, max lengths, read-only), relational integrity (category assignment, supplier linkage), and edge cases (invalid payloads, unauthorized access). Format: Output a detailed Markdown table with columns: Test ID, Endpoint, Method (GET/POST/PUT/PATCH/DELETE), Payload Summary, Expected Status Code, Expected Validation, Test Type. Action: Save the output directly into the test-cases folder as api-manual-tests.md. Append this exact prompt instruction to agents/prompts.md.

## API Automation Setup Workflow

### Step 1: Create Python Dependencies File
Create a requirements.txt file inside the automation/api/ folder containing "pytest" and "requests". Then, create a new directory named "tests" inside automation/api/.

### Step 2: Setup Pytest Fixtures
Inside automation/api/tests/, create a file named conftest.py. Write a pytest fixture in it that provides the base URL "http://localhost:8000/api/part/" and standard basic authentication headers for API testing.

### Step 3: Implement API Test Automation
Inside automation/api/tests/, create a file named test_parts_api.py. Write executable API automation scripts using pytest and requests to cover CRUD operations on Parts. You must include @pytest.mark.parametrize to demonstrate data-driven testing, and include assertions on status codes and response schemas.

## UI Automation Setup Workflow

### Step 1: Create UI Automation Dependencies
Create a requirements.txt file inside the automation/ui/ folder containing "playwright" and "pytest-playwright". Then, create two new directories inside automation/ui/ named "pages" and "tests".

### Step 2: Create BasePage with Playwright Utilities
Inside automation/ui/pages/, create a file named base_page.py with a BasePage class containing common Playwright wrapper methods initialized with a page fixture (e.g., wait_for_selector, click_element using page.locator().click(), and enter_text using page.locator().fill()).

### Step 3: Create LoginPage Implementation
Inside automation/ui/pages/, create a file named login_page.py with a LoginPage class that inherits from BasePage, navigates to "https://demo.inventree.org/accounts/login/", and handles a basic login action.

### Step 4: Implement Login Tests
Inside automation/ui/tests/, create a file named test_login.py. Write a pytest function named test_successful_login that uses the Playwright page fixture from pytest-playwright. Import the LoginPage class, instantiate it with the page fixture, navigate to the URL, and call the login method using the InvenTree demo credentials. Finally, add an assertion to verify the login was successful, such as checking that the page URL has changed or that a dashboard element is visible.
