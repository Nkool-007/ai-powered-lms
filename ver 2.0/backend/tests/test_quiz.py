from tests.conftest import (
    auth_header,
    create_course_with_lesson,
    login_user,
    register_user,
)


def _setup_quiz(client):
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

    course_id, _, _ = create_course_with_lesson(
        client,
        instructor_token,
    )

    create_quiz = client.post(
        f"/api/v1/courses/{course_id}/quizzes",
        headers=auth_header(instructor_token),
        json={
            "title": "Python Basics Quiz",
            "description": "Test fundamentals.",
            "questions": [
                {
                    "question_text": "Which keyword defines a function?",
                    "position": 1,
                    "options": [
                        {
                            "option_text": "function",
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

    assert create_quiz.status_code == 201

    quiz_data = create_quiz.get_json()["data"]
    quiz_id = quiz_data["id"]
    question_id = quiz_data["questions"][0]["id"]
    correct_option = next(
        option
        for option in quiz_data["questions"][0]["options"]
        if option["is_correct"]
    )

    publish = client.patch(
        f"/api/v1/courses/{course_id}/publish",
        headers=auth_header(instructor_token),
    )

    assert publish.status_code == 200

    enroll = client.post(
        f"/api/v1/courses/{course_id}/enroll",
        headers=auth_header(student_token),
    )

    assert enroll.status_code == 201

    return {
        "course_id": course_id,
        "quiz_id": quiz_id,
        "question_id": question_id,
        "correct_option_id": correct_option["id"],
        "instructor_token": instructor_token,
        "student_token": student_token,
    }


def test_course_quiz_listing_endpoint(client):
    setup = _setup_quiz(client)

    response = client.get(
        f"/api/v1/courses/{setup['course_id']}/quizzes",
        headers=auth_header(setup["student_token"]),
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data) == 1
    assert data[0]["id"] == setup["quiz_id"]


def test_student_quiz_does_not_leak_correct_answer(client):
    setup = _setup_quiz(client)

    response = client.get(
        f"/api/v1/quizzes/{setup['quiz_id']}",
        headers=auth_header(setup["student_token"]),
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    for question in data["questions"]:
        for option in question["options"]:
            assert "is_correct" not in option


def test_quiz_submission_is_scored_by_backend(client):
    setup = _setup_quiz(client)

    response = client.post(
        f"/api/v1/quizzes/{setup['quiz_id']}/submit",
        headers=auth_header(setup["student_token"]),
        json={
            "answers": [
                {
                    "question_id": setup["question_id"],
                    "selected_option_id": setup["correct_option_id"],
                }
            ],
            "score": 0,
        },
    )

    assert response.status_code == 201

    data = response.get_json()["data"]

    assert data["score"] == 100.0
    assert data["correct_answers"] == 1
    assert data["total_questions"] == 1


def test_quiz_attempt_history(client):
    setup = _setup_quiz(client)

    submit = client.post(
        f"/api/v1/quizzes/{setup['quiz_id']}/submit",
        headers=auth_header(setup["student_token"]),
        json={
            "answers": [
                {
                    "question_id": setup["question_id"],
                    "selected_option_id": setup["correct_option_id"],
                }
            ],
        },
    )

    assert submit.status_code == 201

    response = client.get(
        "/api/v1/students/me/quiz-attempts",
        headers=auth_header(setup["student_token"]),
    )

    assert response.status_code == 200
    assert len(response.get_json()["data"]) == 1
