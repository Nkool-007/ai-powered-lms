from tests.conftest import (
    auth_header,
    login_user,
    register_user,
)


def test_student_cannot_create_course(client):
    register_user(
        client,
        "Student",
        "student@example.com",
        "STUDENT",
    )

    token = login_user(
        client,
        "student@example.com",
    )

    response = client.post(
        "/api/v1/courses",
        headers=auth_header(token),
        json={
            "title": "Illegal Course",
            "description": "Should fail.",
        },
    )

    assert response.status_code == 403


def test_instructor_can_create_course(client):
    register_user(
        client,
        "Instructor",
        "teacher@example.com",
        "INSTRUCTOR",
    )

    token = login_user(
        client,
        "teacher@example.com",
    )

    response = client.post(
        "/api/v1/courses",
        headers=auth_header(token),
        json={
            "title": "Python",
            "description": "Python course.",
        },
    )

    assert response.status_code == 201


def test_instructor_cannot_edit_another_instructors_course(client):
    register_user(
        client,
        "Instructor A",
        "a@example.com",
        "INSTRUCTOR",
    )
    token_a = login_user(client, "a@example.com")

    course_response = client.post(
        "/api/v1/courses",
        headers=auth_header(token_a),
        json={
            "title": "Owned by A",
            "description": "Course.",
        },
    )
    course_id = course_response.get_json()["data"]["id"]

    register_user(
        client,
        "Instructor B",
        "b@example.com",
        "INSTRUCTOR",
    )
    token_b = login_user(client, "b@example.com")

    response = client.put(
        f"/api/v1/courses/{course_id}",
        headers=auth_header(token_b),
        json={
            "title": "Hijacked",
        },
    )

    assert response.status_code == 403
