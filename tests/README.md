# Tests Directory

This directory contains comprehensive tests for the Mergington High School API using pytest and FastAPI's testing framework.

## Test Structure

- `conftest.py` - Test configuration and fixtures
- `test_app.py` - API endpoint tests including HTTP status codes, response formats, and business logic
- `test_data.py` - Unit tests for data structures and validation

## Test Categories

### API Endpoint Tests (`test_app.py`)
- **Root Endpoint**: Tests redirect functionality
- **Activities Endpoint**: Tests retrieving all activities and data structure
- **Activity Signup**: Tests successful signup, error cases, and edge cases
- **Response Format**: Tests content types and HTTP headers

### Data Structure Tests (`test_data.py`)
- **Database Structure**: Validates activity data format and required fields
- **Data Consistency**: Ensures email domains, participant limits, and data integrity

## Running Tests

### Run all tests:
```bash
pytest tests/ -v
```

### Run with coverage:
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

### Run specific test file:
```bash
pytest tests/test_app.py -v
```

### Run specific test class:
```bash
pytest tests/test_app.py::TestActivitySignup -v
```

## Test Features

- **100% Code Coverage**: All application code is tested
- **Fixtures**: Reusable test data and client setup
- **Edge Case Testing**: Invalid inputs, boundary conditions, and error scenarios
- **Data Validation**: Comprehensive validation of data structures and business rules
- **Isolation**: Tests are isolated and don't affect each other's state

## Dependencies

- `pytest` - Testing framework
- `httpx` - HTTP client for FastAPI testing
- `pytest-cov` - Coverage reporting