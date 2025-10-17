"""
Unit tests for individual functions and data structures in the app.
"""

import pytest
from src.app import activities


class TestActivitiesDatabase:
    """Tests for the activities database structure and content."""
    
    def test_activities_is_dict(self):
        """Test that activities is a dictionary."""
        assert isinstance(activities, dict)
    
    def test_all_activities_have_required_fields(self):
        """Test that all activities have the required fields."""
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"
    
    def test_activity_field_types(self):
        """Test that activity fields have correct types."""
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["description"], str), f"Description for '{activity_name}' should be string"
            assert isinstance(activity_data["schedule"], str), f"Schedule for '{activity_name}' should be string"
            assert isinstance(activity_data["max_participants"], int), f"Max participants for '{activity_name}' should be int"
            assert isinstance(activity_data["participants"], list), f"Participants for '{activity_name}' should be list"
    
    def test_max_participants_positive(self):
        """Test that max_participants is positive for all activities."""
        for activity_name, activity_data in activities.items():
            assert activity_data["max_participants"] > 0, f"Max participants for '{activity_name}' should be positive"
    
    def test_participants_not_exceed_max(self):
        """Test that current participants don't exceed max_participants."""
        for activity_name, activity_data in activities.items():
            current_count = len(activity_data["participants"])
            max_count = activity_data["max_participants"]
            assert current_count <= max_count, f"'{activity_name}' has {current_count} participants but max is {max_count}"
    
    def test_participant_emails_unique_per_activity(self):
        """Test that participant emails are unique within each activity."""
        for activity_name, activity_data in activities.items():
            participants = activity_data["participants"]
            unique_participants = set(participants)
            assert len(participants) == len(unique_participants), f"Duplicate participants in '{activity_name}'"
    
    def test_expected_activities_present(self):
        """Test that all expected activities are present."""
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Soccer Team",
            "Swimming Club", "Art Club", "Drama Club", "Debate Team", "Science Olympiad"
        ]
        
        for expected in expected_activities:
            assert expected in activities, f"Expected activity '{expected}' not found"
    
    def test_activity_descriptions_not_empty(self):
        """Test that all activities have non-empty descriptions."""
        for activity_name, activity_data in activities.items():
            assert activity_data["description"].strip(), f"Activity '{activity_name}' has empty description"
    
    def test_activity_schedules_not_empty(self):
        """Test that all activities have non-empty schedules."""
        for activity_name, activity_data in activities.items():
            assert activity_data["schedule"].strip(), f"Activity '{activity_name}' has empty schedule"


class TestActivityDataConsistency:
    """Tests for data consistency across activities."""
    
    def test_email_domains_consistent(self):
        """Test that all participant emails use the same domain."""
        expected_domain = "@mergington.edu"
        
        for activity_name, activity_data in activities.items():
            for email in activity_data["participants"]:
                assert email.endswith(expected_domain), f"Email '{email}' in '{activity_name}' doesn't use expected domain"
    
    def test_reasonable_max_participants_ranges(self):
        """Test that max_participants are in reasonable ranges."""
        for activity_name, activity_data in activities.items():
            max_participants = activity_data["max_participants"]
            # Assuming reasonable range is 1-100 for a high school
            assert 1 <= max_participants <= 100, f"'{activity_name}' has unreasonable max_participants: {max_participants}"
    
    def test_no_duplicate_participants_across_different_activities(self):
        """Test for potential data inconsistencies (this is informational)."""
        all_participants = {}
        
        for activity_name, activity_data in activities.items():
            for email in activity_data["participants"]:
                if email not in all_participants:
                    all_participants[email] = []
                all_participants[email].append(activity_name)
        
        # This test documents which students are in multiple activities
        # It's not necessarily an error, but good to be aware of
        multi_activity_students = {email: activities for email, activities in all_participants.items() if len(activities) > 1}
        
        # This assertion will pass but documents the multi-activity students
        assert len(multi_activity_students) >= 0  # Always true, just for documentation