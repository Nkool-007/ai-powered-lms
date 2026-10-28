from tests.conftest import (
    auth_header,
    create_course_with_lesson,
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
    assert (
        response.get_json()["error"]
        == "INSUFFICIENT_PERMISSION"
    )


def test_instructor_can_create_course(client):
    register_user(
        client,
        "Instructor",
        "instructor@example.com",
        "INSTRUCTOR",
    )

    token = login_user(
        client,
        "instructor@example.com",
    )

    response = client.post(
        "/api/v1/courses",
        headers=auth_header(token),
        json={
            "title": "Course",
            "description": "Valid course.",
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
    register_user(
        client,
        "Instructor B",
        "b@example.com",
        "INSTRUCTOR",
    )

    token_a = login_user(client, "a@example.com")
    token_b = login_user(client, "b@example.com")

    course_id, _, _ = create_course_with_lesson(
        client,
        token_a,
    )

    response = client.put(
        f"/api/v1/courses/{course_id}",
        headers=auth_header(token_b),
        json={
            "title": "Hijacked",
        },
    )

    assert response.status_code == 403
    assert response.get_json()["error"] == "NOT_COURSE_OWNER"
