from tests.conftest import (
    auth_header,
    create_course_with_lesson,
    login_user,
    register_user,
)


def _setup_published_course_and_student(client):
    register_user(
        client,
        "Instructor",
        "instructor@example.com",
        "INSTRUCTOR",
    )
    register_user(
        client,
        "Student",
        "student@example.com",
        "STUDENT",
    )

    instructor_token = login_user(
        client,
        "instructor@example.com",
    )
    student_token = login_user(
        client,
        "student@example.com",
    )

    course_id, _, lesson_id = create_course_with_lesson(
        client,
        instructor_token,
    )

    publish_response = client.patch(
        f"/api/v1/courses/{course_id}/publish",
        headers=auth_header(instructor_token),
    )

    assert publish_response.status_code == 200

    return (
        course_id,
        lesson_id,
        instructor_token,
        student_token,
    )


def test_student_enrolls_and_duplicate_rejected(client):
    course_id, _, _, student_token = (
        _setup_published_course_and_student(client)
    )

    response = client.post(
        f"/api/v1/courses/{course_id}/enroll",
        headers=auth_header(student_token),
    )

    assert response.status_code == 201

    duplicate = client.post(
        f"/api/v1/courses/{course_id}/enroll",
        headers=auth_header(student_token),
    )

    assert duplicate.status_code == 409
    assert duplicate.get_json()["error"] == "ALREADY_ENROLLED"


def test_unenrolled_student_cannot_access_lesson(client):
    course_id, lesson_id, _, _ = (
        _setup_published_course_and_student(client)
    )

    register_user(
        client,
        "Student B",
        "studentb@example.com",
        "STUDENT",
    )

    token_b = login_user(
        client,
        "studentb@example.com",
    )

    response = client.get(
        f"/api/v1/lessons/{lesson_id}",
        headers=auth_header(token_b),
    )

    assert response.status_code == 403
    assert (
        response.get_json()["error"]
        == "COURSE_ENROLLMENT_REQUIRED"
    )


def test_complete_lesson_is_idempotent_and_progress_is_calculated(client):
    course_id, lesson_id, _, student_token = (
        _setup_published_course_and_student(client)
    )

    enroll = client.post(
        f"/api/v1/courses/{course_id}/enroll",
        headers=auth_header(student_token),
    )

    assert enroll.status_code == 201

    first = client.post(
        f"/api/v1/lessons/{lesson_id}/complete",
        headers=auth_header(student_token),
    )

    second = client.post(
        f"/api/v1/lessons/{lesson_id}/complete",
        headers=auth_header(student_token),
    )

    assert first.status_code == 200
    assert second.status_code == 200

    progress = client.get(
        f"/api/v1/courses/{course_id}/progress",
        headers=auth_header(student_token),
    )

    assert progress.status_code == 200

    data = progress.get_json()["data"]

    assert data["completed_lessons"] == 1
    assert data["total_lessons"] == 1
    assert data["progress_percentage"] == 100.0
