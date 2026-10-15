import os

import pytest

from app import create_app
from app.extensions import db


@pytest.fixture()
def app():
    database_url = os.getenv(
        "TEST_DATABASE_URL",
        "sqlite:///:memory:",
    )

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": database_url,
            "JWT_SECRET_KEY": "test-secret-key",
        }
    )

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def register_user(
    client,
    name,
    email,
    role,
    password="Password123",
):
    return client.post(
        "/api/v1/auth/register",
        json={
            "name": name,
            "email": email,
            "password": password,
            "role": role,
        },
    )


def login_user(
    client,
    email,
    password="Password123",
):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    return response.get_json()["data"]["access_token"]


def auth_header(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def create_published_course_with_lesson(client, instructor_token):
    course_response = client.post(
        "/api/v1/courses",
        headers=auth_header(instructor_token),
        json={
            "title": "Python Fundamentals",
            "description": "Python course.",
        },
    )
    course_id = course_response.get_json()["data"]["id"]

    module_response = client.post(
        f"/api/v1/courses/{course_id}/modules",
        headers=auth_header(instructor_token),
        json={
            "title": "Basics",
            "description": "Core concepts",
            "position": 1,
        },
    )
    module_id = module_response.get_json()["data"]["id"]

    lesson_response = client.post(
        f"/api/v1/modules/{module_id}/lessons",
        headers=auth_header(instructor_token),
        json={
            "title": "Variables",
            "content": "Lesson body.",
            "position": 1,
        },
    )
    lesson_id = lesson_response.get_json()["data"]["id"]

    publish_response = client.patch(
        f"/api/v1/courses/{course_id}/publish",
        headers=auth_header(instructor_token),
    )
    assert publish_response.status_code == 200

    return course_id, module_id, lesson_id
