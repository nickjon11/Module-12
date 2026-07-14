def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "username": "jonathan",
            "email": "jonathan@example.com",
            "password": "SecurePassword123!",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "jonathan"
    assert data["email"] == "jonathan@example.com"
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data
    assert "password_hash" not in data


def test_duplicate_username_is_rejected(client):
    first_user = {
        "username": "jonathan",
        "email": "first@example.com",
        "password": "SecurePassword123!",
    }

    second_user = {
        "username": "jonathan",
        "email": "second@example.com",
        "password": "SecurePassword456!",
    }

    first_response = client.post("/users", json=first_user)
    second_response = client.post("/users", json=second_user)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Username already exists."


def test_duplicate_email_is_rejected(client):
    first_user = {
        "username": "jonathan1",
        "email": "duplicate@example.com",
        "password": "SecurePassword123!",
    }

    second_user = {
        "username": "jonathan2",
        "email": "duplicate@example.com",
        "password": "SecurePassword456!",
    }

    first_response = client.post("/users", json=first_user)
    second_response = client.post("/users", json=second_user)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Email already exists."


def test_invalid_email_returns_422(client):
    response = client.post(
        "/users",
        json={
            "username": "jonathan",
            "email": "invalid-email",
            "password": "SecurePassword123!",
        },
    )

    assert response.status_code == 422


def test_short_password_returns_422(client):
    response = client.post(
        "/users",
        json={
            "username": "jonathan",
            "email": "jonathan@example.com",
            "password": "short",
        },
    )

    assert response.status_code == 422
