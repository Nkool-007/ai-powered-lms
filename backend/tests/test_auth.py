from tests.conftest import login_user, register_user


def test_successful_registration(client):
    response = register_user(
        client,
        "Aman",
        "aman@example.com",
        "STUDENT",
    )

    assert response.status_code == 201

    data = response.get_json()["data"]

    assert data["email"] == "aman@example.com"
    assert "password_hash" not in data


def test_duplicate_email_rejected(client):
    register_user(
        client,
        "Aman",
        "aman@example.com",
        "STUDENT",
    )

    response = register_user(
        client,
        "Another Aman",
        "aman@example.com",
        "STUDENT",
    )

    assert response.status_code == 409


def test_successful_login(client):
    register_user(
        client,
        "Aman",
        "aman@example.com",
        "STUDENT",
    )

    token = login_user(
        client,
        "aman@example.com",
    )

    assert token


def test_incorrect_password_rejected(client):
    register_user(
        client,
        "Aman",
        "aman@example.com",
        "STUDENT",
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "aman@example.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401


def test_missing_jwt_rejected(client):
    response = client.get(
        "/api/v1/auth/me"
    )

    assert response.status_code == 401
