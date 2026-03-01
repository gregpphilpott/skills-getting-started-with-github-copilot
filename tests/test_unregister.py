from urllib.parse import quote


def test_unregister_removes_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": existing_email},
    )
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    assert existing_email not in participants


def test_unregister_rejects_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "not-registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": missing_email},
    )

    # Assert
    assert response.status_code == 404
    assert "not signed up" in response.json()["detail"]


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    unknown_activity = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{quote(unknown_activity)}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
