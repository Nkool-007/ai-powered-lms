from tests.conftest import (
    auth_header,
    create_published_course_with_lesson,
    login_user,
    register_user,
)


def test_enrollment_duplicate_and_progress_flow(client):
    register_user(
        client,
        "Instructor",
        "teacher@example.com",
        "INSTRUCTOR",
    )
    instructor_token = login_user(
        client,
        "teacher@example.com",
    )

    course_id, _, lesson_id = create_published_course_with_lesson(
        client,
        instructor_token,
    )

    register_user(
        client,
        "Student",
        "student@example.com",
        "STUDENT",
    )
    student_token = login_user(
        client,
        "student@example.com",
    )

    enroll_response = client.post(
        f"/api/v1/courses/{course_id}/enroll",
        headers=auth_header(student_token),
    )
    assert enroll_response.status_code == 201

    duplicate_response = client.post(
        f"/api/v1/courses/{course_id}/enroll",
        headers=auth_header(student_token),
    )
    assert duplicate_response.status_code == 409

    complete_response = client.post(
        f"/api/v1/lessons/{lesson_id}/complete",
        headers=auth_header(student_token),
    )
    assert complete_response.status_code == 200

    complete_again_response = client.post(
        f"/api/v1/lessons/{lesson_id}/complete",
        headers=auth_header(student_token),
    )
    assert complete_again_response.status_code == 200

    progress_response = client.get(
        f"/api/v1/courses/{course_id}/progress",
        headers=auth_header(student_token),
    )

    assert progress_response.status_code == 200

    data = progress_response.get_json()["data"]

    assert data["completed_lessons"] == 1
    assert data["total_lessons"] == 1
    assert data["progress_percentage"] == 100.0
