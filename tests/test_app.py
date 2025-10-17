"""
Tests for the FastAPI application endpoints.
"""

import pytest
from fastapi import status


class TestRootEndpoint:
    """Tests for the root endpoint."""
    
    def test_root_redirects_to_static_index(self, client):
        """Test that root endpoint redirects to static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.headers["location"] == "/static/index.html"


class TestActivitiesEndpoint:
    """Tests for the activities endpoint."""
    
    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all available activities."""
        response = client.get("/activities")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        
        # Check that known activities are present
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Soccer Team",
            "Swimming Club", "Art Club", "Drama Club", "Debate Team", "Science Olympiad"
        ]
        for activity in expected_activities:
            assert activity in data
    
    def test_activity_structure(self, client):
        """Test that each activity has the correct structure."""
        response = client.get("/activities")
        data = response.json()
        
        # Test the structure of the first activity
        activity_name = list(data.keys())[0]
        activity = data[activity_name]
        
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        
        assert isinstance(activity["description"], str)
        assert isinstance(activity["schedule"], str)
        assert isinstance(activity["max_participants"], int)
        assert isinstance(activity["participants"], list)


class TestActivitySignup:
    """Tests for activity signup functionality."""
    
    def test_successful_signup(self, client, reset_activities):
        """Test successful signup for an activity."""
        email = "newstudent@mergington.edu"
        activity_name = "Chess Club"
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == f"Signed up {email} for {activity_name}"
        
        # Verify the student was added to the activity
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]
    
    def test_signup_nonexistent_activity(self, client):
        """Test signup for a non-existent activity returns 404."""
        email = "student@mergington.edu"
        activity_name = "Nonexistent Activity"
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_duplicate_signup(self, client, reset_activities):
        """Test that duplicate signup returns 400 error."""
        # First, get an existing participant
        activities_response = client.get("/activities")
        activities = activities_response.json()
        
        activity_name = "Chess Club"
        existing_email = activities[activity_name]["participants"][0]
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert data["detail"] == "Student is already signed up for this activity"
    
    def test_signup_with_spaces_in_activity_name(self, client, reset_activities):
        """Test signup for activity with spaces in name."""
        email = "newstudent@mergington.edu"
        activity_name = "Programming Class"
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == f"Signed up {email} for {activity_name}"


class TestActivitySignupEdgeCases:
    """Tests for edge cases in activity signup."""
    
    def test_signup_with_invalid_email_format(self, client, reset_activities):
        """Test signup with various email formats (API doesn't validate format)."""
        # The API doesn't validate email format, so this should still work
        email = "invalid-email"
        activity_name = "Chess Club"
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_signup_with_empty_email(self, client):
        """Test signup with empty email."""
        activity_name = "Chess Club"
        
        response = client.post(f"/activities/{activity_name}/signup")
        
        # Should return 422 for missing required parameter
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_multiple_signups_different_activities(self, client, reset_activities):
        """Test that a student can sign up for multiple different activities."""
        email = "multisport@mergington.edu"
        
        # Sign up for Chess Club
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response1.status_code == status.HTTP_200_OK
        
        # Sign up for Programming Class
        response2 = client.post(
            "/activities/Programming Class/signup",
            params={"email": email}
        )
        assert response2.status_code == status.HTTP_200_OK
        
        # Verify both signups
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Programming Class"]["participants"]


class TestAPIResponseFormat:
    """Tests for API response formats and headers."""
    
    def test_activities_response_content_type(self, client):
        """Test that activities endpoint returns JSON content type."""
        response = client.get("/activities")
        assert response.headers["content-type"] == "application/json"
    
    def test_signup_response_content_type(self, client, reset_activities):
        """Test that signup endpoint returns JSON content type."""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.headers["content-type"] == "application/json"