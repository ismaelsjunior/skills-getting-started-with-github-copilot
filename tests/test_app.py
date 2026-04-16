import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_root():
    # Arrange
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code == 200
    assert "Mergington High School" in response.text

def test_get_activities():
    # Arrange
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_for_activity_success():
    # Arrange
    activity = "Basketball Team"
    email = "test@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]
    # Check if added
    resp = client.get("/activities")
    data = resp.json()
    assert email in data[activity]["participants"]

def test_signup_for_activity_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already in
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"]

def test_signup_for_activity_not_found():
    # Arrange
    activity = "Nonexistent Activity"
    email = "test@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]

def test_remove_participant_success():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Removed" in result["message"]
    # Check if removed
    resp = client.get("/activities")
    data = resp.json()
    assert email not in data[activity]["participants"]

def test_remove_participant_not_found():
    # Arrange
    activity = "Chess Club"
    email = "nonexistent@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Participant not found" in result["detail"]

def test_remove_participant_activity_not_found():
    # Arrange
    activity = "Nonexistent Activity"
    email = "test@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]