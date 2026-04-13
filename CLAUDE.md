# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agentic-QA-InvenTree is a QA automation project for testing InvenTree (an open-source inventory management system), utilizing AI agents to enhance test automation capabilities.

## Repository Structure

```
├── agents/          # AI agent implementations for test generation, execution, and analysis
├── test-cases/      # Test case definitions and specifications
├── automation/
│   ├── ui/         # UI test automation (browser-based tests)
│   └── api/        # API test automation (REST API tests)
└── video/          # Test execution recordings and demo videos
```

## Architecture

### Agents Directory
Contains AI agent code that can:
- Generate test cases based on application analysis
- Execute and orchestrate test runs
- Analyze test results and failures
- Suggest test improvements

### Test Cases Directory
Stores test case definitions, which may include:
- Test scenarios and user stories
- Expected behaviors and acceptance criteria
- Test data requirements

### Automation Directory
- **UI tests**: Browser automation targeting InvenTree's web interface
- **API tests**: REST API tests for InvenTree's backend endpoints

### Video Directory
Stores visual records of test executions for debugging and documentation purposes.

## InvenTree Context

InvenTree is an open-source inventory management system with:
- Web-based UI
- REST API
- Features: inventory tracking, BOM management, purchasing, stock location management
- Tech stack: Django (Python), PostgreSQL, REST framework

When writing tests, consider InvenTree's core workflows:
- Part and inventory management
- Stock movements and locations
- Purchase orders and suppliers
- Build orders and manufacturing

## Development Workflow

This is a new project. As you add code:
- Place agent implementations in `agents/`
- Store test definitions in `test-cases/`
- Implement UI automation in `automation/ui/`
- Implement API automation in `automation/api/`
- Save test recordings in `video/`

Update this file with specific build commands, test execution instructions, and dependencies as the project evolves.
