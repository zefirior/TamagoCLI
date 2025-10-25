# Tests

This directory contains all tests for the Tamagochi game.

## Test Structure

```
tests/
├── __init__.py
├── test_eating_timer.py    # Tests for eating timer functionality
└── test_pet_model.py        # Tests for Pet model
```

## Running Tests

### Run all tests
```bash
uv run pytest
```

### Run specific test file
```bash
uv run pytest tests/test_eating_timer.py
```

### Run specific test class
```bash
uv run pytest tests/test_eating_timer.py::TestEatingTimer
```

### Run specific test
```bash
uv run pytest tests/test_eating_timer.py::TestEatingTimer::test_eating_starts_correctly
```

### Run with verbose output
```bash
uv run pytest -v
```

### Run with coverage
```bash
uv run pytest --cov=tamagochi --cov-report=html
```

### Run with markers
```bash
# Run only slow tests
uv run pytest -m slow

# Run everything except slow tests
uv run pytest -m "not slow"
```

## Test Categories

### TestEatingTimer
Tests for the 3-second eating timer:
- Eating starts correctly
- Finishes after 3 seconds
- Duration tracking
- Cannot feed twice
- Game loop simulation
- Old save compatibility

### TestEatingActions
Tests for actions during eating:
- Cannot play while eating
- Cannot sleep while eating
- Cannot heal while eating
- Actions available after eating

### TestEatingStats
Tests for stat changes:
- Hunger increases after feeding
- Happiness increases after feeding
- Cannot feed when full

### TestPetCreation
Tests for pet creation:
- Basic creation
- All pet types
- Initial stats

### TestPetStats
Tests for pet statistics:
- Stats bounds (0-100)
- Alive/dead logic

### TestPetActions
Tests for pet actions:
- Feed, play, sleep, wake up, heal

### TestPetSerialization
Tests for save/load:
- to_dict()
- from_dict()
- Roundtrip save/load

## Adding New Tests

1. Create new test file in `tests/` directory
2. Name it `test_*.py`
3. Create test classes with `Test*` prefix
4. Create test methods with `test_*` prefix

Example:
```python
import pytest
from tamagochi.models.pet import Pet, PetType

class TestNewFeature:
    def test_something(self):
        pet = Pet("Test", PetType.CAT)
        assert pet.name == "Test"
```

## CI/CD

Tests run automatically on:
- Push to main branch
- Pull requests
- Manual trigger

## Coverage

Current coverage: **~90%** of core logic

To generate coverage report:
```bash
uv run pytest --cov=tamagochi --cov-report=html
open htmlcov/index.html
```

