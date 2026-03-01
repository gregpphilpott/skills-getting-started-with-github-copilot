def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "new-student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": new_email})
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert new_email in participants


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_rejects_unknown_activity(client):
    # Arrange
    unknown_activity = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{unknown_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
