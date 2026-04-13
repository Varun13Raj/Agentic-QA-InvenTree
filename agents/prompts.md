# Agent Prompts

## UI Manual Test Case Generation for InvenTree Parts Module

Act as a Senior Quality Engineering Architect. I need you to ingest the InvenTree Parts documentation from https://docs.inventree.org/en/stable/part/ (including sub-pages like Part Views, Parameters, Templates, Revisions). Generate a comprehensive suite of manual UI test cases specifically for the Parts module covering creation, all detail view tabs, categories, and revisions, including negative and boundary scenarios. Output the test cases as a detailed Markdown table with columns: Test ID, Module, Scenario Description, Steps to Reproduce, Expected Result, Test Type (Positive/Negative/Boundary). Action: Save the final markdown table directly into the test-cases folder as ui-manual-tests.md. Also, save this exact prompt instruction into the agents folder as a file named prompts.md.

## API Manual Test Case Generation for InvenTree Parts Module

Act as a Senior API Test Architect. Based on the InvenTree API schema for the Parts module, generate a comprehensive suite of manual API test cases. Constraints: - Must cover: CRUD operations on Parts and Part Categories. - Must include: Filtering, pagination, and search on the Parts list endpoint. - Must test: Field-level validation (required, max lengths, read-only), relational integrity (category assignment, supplier linkage), and edge cases (invalid payloads, unauthorized access). Format: Output a detailed Markdown table with columns: Test ID, Endpoint, Method (GET/POST/PUT/PATCH/DELETE), Payload Summary, Expected Status Code, Expected Validation, Test Type. Action: Save the output directly into the test-cases folder as api-manual-tests.md. Append this exact prompt instruction to agents/prompts.md.
