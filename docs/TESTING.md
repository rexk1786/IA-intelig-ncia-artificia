# Testing Guide

## Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific file
pytest tests/unit/test_auth_service.py

# Docker
docker-compose exec app pytest
```

## Test Structure

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── fixtures/       # Test data
└── conftest.py     # Configuration
```

## Writing Tests

Use AAA pattern: Arrange, Act, Assert

```python
def test_example():
    # Arrange
    data = {"key": "value"}
    
    # Act
    result = function(data)
    
    # Assert
    assert result is not None
```
