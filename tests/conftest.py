"""
Test configuration and fixtures for the FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_activity():
    """Sample activity data for testing."""
    return {
        "description": "Test activity description",
        "schedule": "Test schedule",
        "max_participants": 10,
        "participants": ["test1@mergington.edu", "test2@mergington.edu"]
    }


@pytest.fixture
def reset_activities():
    """Reset the activities database to its original state after each test."""
    # Store original activities
    from src.app import activities
    original_activities = {}
    for name, activity in activities.items():
        original_activities[name] = {
            "description": activity["description"],
            "schedule": activity["schedule"],
            "max_participants": activity["max_participants"],
            "participants": activity["participants"].copy()
        }
    
    yield
    
    # Reset activities to original state
    activities.clear()
    activities.update(original_activities)