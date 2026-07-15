import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    original_activities = copy.deepcopy(activities)

    with TestClient(app) as test_client:
        yield test_client

    activities.clear()
    activities.update(copy.deepcopy(original_activities))


def test_root_redirects_to_static_index(client):
    # Arrange

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_list_activities_returns_registered_activity_data(client):
    # Arrange

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in payload
    assert payload["Chess Club"]["max_participants"] == 12
    assert "michael@mergington.edu" in payload["Chess Club"]["participants"]


def test_signup_adds_student_to_activity(client):
    # Arrange
    email = "new.student@mergington.edu"

    # Act
    response = client.post("/activities/Gym%20Class/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in activities["Gym Class"]["participants"]


def test_unregister_removes_student_from_activity(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/Chess%20Club/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]
