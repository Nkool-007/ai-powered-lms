from tests.conftest import (
    auth_header,
    login_user,
    register_user,
)


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
    assert data["role"] == "STUDENT"
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
        "Aman Again",
        "AMAN@example.com",
        "STUDENT",
    )

    assert response.status_code == 409
    assert (
        response.get_json()["error"]
        == "EMAIL_ALREADY_REGISTERED"
    )


def test_login_and_me(client):
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

    response = client.get(
        "/api/v1/auth/me",
        headers=auth_header(token),
    )

    assert response.status_code == 200
    assert response.get_json()["data"]["email"] == "aman@example.com"


def test_wrong_password_rejected(client):
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
            "password": "WrongPassword123",
        },
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "INVALID_CREDENTIALS"


def test_missing_jwt_uses_standard_error(client):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401
    assert (
        response.get_json()["error"]
        == "AUTHENTICATION_REQUIRED"
    )
