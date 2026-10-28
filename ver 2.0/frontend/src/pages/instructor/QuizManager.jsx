import {
  useEffect,
  useState,
} from "react";

import {
  Link,
  useParams,
} from "react-router-dom";

import quizService from "../../services/quizService";
import { getErrorMessage } from "../../utils/errors";

import Button from "../../components/common/Button";
import ErrorState from "../../components/common/ErrorState";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import EmptyState from "../../components/common/EmptyState";

function emptyQuestion(position) {
  return {
    question_text: "",
    position,
    options: [
      {
        option_text: "",
        position: 1,
        is_correct: true,
      },
      {
        option_text: "",
        position: 2,
        is_correct: false,
      },
      {
        option_text: "",
        position: 3,
        is_correct: false,
      },
      {
        option_text: "",
        position: 4,
        is_correct: false,
      },
    ],
  };
}

export default function QuizManager() {
  const { courseId } = useParams();

  const [title, setTitle] =
    useState("");
  const [description, setDescription] =
    useState("");
  const [
    questions,
    setQuestions,
  ] = useState([
    emptyQuestion(1),
  ]);
  const [quizzes, setQuizzes] =
    useState([]);
  const [listLoading, setListLoading] =
    useState(true);
  const [createdQuiz, setCreatedQuiz] =
    useState(null);
  const [error, setError] =
    useState("");
  const [loading, setLoading] =
    useState(false);

  async function loadQuizzes() {
    try {
      setListLoading(true);
      setError("");

      const data =
        await quizService.getCourseQuizzes(
          courseId
        );

      setQuizzes(data);
    } catch (err) {
      setError(
        getErrorMessage(
          err,
          "Unable to load quizzes."
        )
      );
    } finally {
      setListLoading(false);
    }
  }

  useEffect(() => {
    loadQuizzes();
  }, [courseId]);

  function updateQuestion(
    qIndex,
    value
  ) {
    const next = [...questions];

    next[qIndex] = {
      ...next[qIndex],
      question_text: value,
    };

    setQuestions(next);
  }

  function updateOption(
    qIndex,
    oIndex,
    value
  ) {
    const next =
      structuredClone(questions);

    next[qIndex].options[
      oIndex
    ].option_text = value;

    setQuestions(next);
  }

  function selectCorrect(
    qIndex,
    oIndex
  ) {
    const next =
      structuredClone(questions);

    next[qIndex].options =
      next[qIndex].options.map(
        (option, index) => ({
          ...option,
          is_correct:
            index === oIndex,
        })
      );

    setQuestions(next);
  }

  function addQuestion() {
    setQuestions([
      ...questions,
      emptyQuestion(
        questions.length + 1
      ),
    ]);
  }

  function removeQuestion(qIndex) {
    if (questions.length === 1) {
      return;
    }

    const next = questions
      .filter(
        (_, index) =>
          index !== qIndex
      )
      .map(
        (question, index) => ({
          ...question,
          position: index + 1,
        })
      );

    setQuestions(next);
  }

  function validate() {
    if (!title.trim()) {
      return "Quiz title is required.";
    }

    for (const question of questions) {
      if (!question.question_text.trim()) {
        return "Every question needs text.";
      }

      if (
        question.options.some(
          (option) =>
            !option.option_text.trim()
        )
      ) {
        return "Every answer option needs text.";
      }

      if (
        question.options.filter(
          (option) =>
            option.is_correct
        ).length !== 1
      ) {
        return "Every question must have exactly one correct answer.";
      }
    }

    return "";
  }

  async function submit(event) {
    event.preventDefault();

    setError("");
    setCreatedQuiz(null);

    const validationError =
      validate();

    if (validationError) {
      setError(validationError);
      return;
    }

    try {
      setLoading(true);

      const quiz =
        await quizService.createQuiz(
          courseId,
          {
            title: title.trim(),
            description:
              description.trim(),
            questions,
          }
        );

      setCreatedQuiz(quiz);
      setTitle("");
      setDescription("");
      setQuestions([
        emptyQuestion(1),
      ]);

      await loadQuizzes();
    } catch (err) {
      setError(
        getErrorMessage(
          err,
          "Unable to create quiz."
        )
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <div className="d-flex justify-content-between align-items-center flex-wrap gap-3 mb-4">
        <h1 className="h2 mb-0">
          Quiz Manager
        </h1>

        <Link
          to={
            `/instructor/courses/` +
            `${courseId}/edit`
          }
          className="btn btn-outline-secondary"
        >
          Back to Course
        </Link>
      </div>

      {error && (
        <ErrorState message={error} />
      )}

      {createdQuiz && (
        <div className="alert alert-success">
          Quiz “{createdQuiz.title}”
          was created successfully.
        </div>
      )}

      <section className="card mb-5">
        <div className="card-body">
          <h2 className="h4">
            Existing Quizzes
          </h2>

          {listLoading ? (
            <LoadingSpinner text="Loading quizzes..." />
          ) : quizzes.length === 0 ? (
            <EmptyState
              title="No Quizzes"
              message="Create the first quiz for this course."
            />
          ) : (
            <div className="list-group">
              {quizzes.map((quiz) => (
                <div
                  key={quiz.id}
                  className="list-group-item"
                >
                  <strong>
                    {quiz.title}
                  </strong>
                  {quiz.description && (
                    <div className="small text-secondary">
                      {quiz.description}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      <form onSubmit={submit}>
        <div className="card mb-4">
          <div className="card-body">
            <h2 className="h4">
              Create Quiz
            </h2>

            <label className="form-label">
              Quiz Title
            </label>
            <input
              className="form-control mb-3"
              value={title}
              onChange={(event) =>
                setTitle(
                  event.target.value
                )
              }
              required
            />

            <label className="form-label">
              Description
            </label>
            <textarea
              className="form-control"
              rows="3"
              value={description}
              onChange={(event) =>
                setDescription(
                  event.target.value
                )
              }
            />
          </div>
        </div>

        {questions.map(
          (question, qIndex) => (
            <section
              className="card mb-4"
              key={qIndex}
            >
              <div className="card-body">
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <h2 className="h5 mb-0">
                    Question {qIndex + 1}
                  </h2>

                  {questions.length > 1 && (
                    <button
                      type="button"
                      className="btn btn-outline-danger btn-sm"
                      onClick={() =>
                        removeQuestion(
                          qIndex
                        )
                      }
                    >
                      Remove
                    </button>
                  )}
                </div>

                <textarea
                  className="form-control mb-3"
                  rows="2"
                  placeholder="Question text"
                  value={
                    question.question_text
                  }
                  onChange={(event) =>
                    updateQuestion(
                      qIndex,
                      event.target.value
                    )
                  }
                  required
                />

                {question.options.map(
                  (option, oIndex) => (
                    <div
                      className="input-group mb-2"
                      key={oIndex}
                    >
                      <span className="input-group-text">
                        <input
                          className="form-check-input mt-0"
                          type="radio"
                          name={
                            `correct-${qIndex}`
                          }
                          checked={
                            option.is_correct
                          }
                          onChange={() =>
                            selectCorrect(
                              qIndex,
                              oIndex
                            )
                          }
                          aria-label="Correct answer"
                        />
                      </span>

                      <input
                        className="form-control"
                        placeholder={
                          `Option ${oIndex + 1}`
                        }
                        value={
                          option.option_text
                        }
                        onChange={(event) =>
                          updateOption(
                            qIndex,
                            oIndex,
                            event.target.value
                          )
                        }
                        required
                      />
                    </div>
                  )
                )}
              </div>
            </section>
          )
        )}

        <div className="d-flex gap-2 flex-wrap">
          <button
            type="button"
            className="btn btn-outline-primary"
            onClick={addQuestion}
          >
            + Add Question
          </button>

          <Button
            type="submit"
            loading={loading}
          >
            Save Quiz
          </Button>
        </div>
      </form>
    </>
  );
}
