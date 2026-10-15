from tests.conftest import (
    auth_header,
    create_published_course_with_lesson,
    login_user,
    register_user,
)


def test_student_quiz_response_hides_answers_and_submission_scores(client):
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

    course_id, _, _ = create_published_course_with_lesson(
        client,
        instructor_token,
    )

    quiz_response = client.post(
        f"/api/v1/courses/{course_id}/quizzes",
        headers=auth_header(instructor_token),
        json={
            "title": "Python Quiz",
            "description": "One question.",
            "questions": [
                {
                    "question_text": "Which keyword defines a function?",
                    "position": 1,
                    "options": [
                        {
                            "option_text": "func",
                            "position": 1,
                            "is_correct": False,
                        },
                        {
                            "option_text": "def",
                            "position": 2,
                            "is_correct": True,
                        },
                    ],
                }
            ],
        },
    )

    assert quiz_response.status_code == 201

    quiz_data = quiz_response.get_json()["data"]
    quiz_id = quiz_data["id"]
    question = quiz_data["questions"][0]
    question_id = question["id"]

    correct_option_id = next(
        option["id"]
        for option in question["options"]
        if option["is_correct"]
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

    student_quiz_response = client.get(
        f"/api/v1/quizzes/{quiz_id}",
        headers=auth_header(student_token),
    )

    assert student_quiz_response.status_code == 200

    student_quiz = student_quiz_response.get_json()["data"]

    for option in student_quiz["questions"][0]["options"]:
        assert "is_correct" not in option

    submit_response = client.post(
        f"/api/v1/quizzes/{quiz_id}/submit",
        headers=auth_header(student_token),
        json={
            "answers": [
                {
                    "question_id": question_id,
                    "selected_option_id": correct_option_id,
                }
            ]
        },
    )

    assert submit_response.status_code == 201
    assert submit_response.get_json()["data"]["score"] == 100.0

    attempts_response = client.get(
        "/api/v1/students/me/quiz-attempts",
        headers=auth_header(student_token),
    )

    assert attempts_response.status_code == 200
    assert len(attempts_response.get_json()["data"]) == 1
