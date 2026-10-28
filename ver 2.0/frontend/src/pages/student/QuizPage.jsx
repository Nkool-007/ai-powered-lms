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

import Quiz from "../../components/quiz/Quiz";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import ErrorState from "../../components/common/ErrorState";

export default function QuizPage() {
  const { quizId } = useParams();

  const [quiz, setQuiz] =
    useState(null);
  const [
    selectedAnswers,
    setSelectedAnswers,
  ] = useState({});
  const [result, setResult] =
    useState(null);
  const [loading, setLoading] =
    useState(true);
  const [submitting, setSubmitting] =
    useState(false);
  const [error, setError] =
    useState("");

  async function load() {
    try {
      setLoading(true);
      setError("");

      const data =
        await quizService.getQuiz(quizId);

      setQuiz(data);
    } catch (err) {
      setError(
        getErrorMessage(
          err,
          "Unable to load quiz."
        )
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, [quizId]);

  async function submit() {
    if (
      Object.keys(
        selectedAnswers
      ).length !==
      quiz.questions.length
    ) {
      setError(
        "Please answer every question before submitting."
      );
      return;
    }

    const answers =
      Object.entries(
        selectedAnswers
      ).map(
        ([
          questionId,
          optionId,
        ]) => ({
          question_id:
            Number(questionId),
          selected_option_id:
            Number(optionId),
        })
      );

    try {
      setSubmitting(true);
      setError("");

      const data =
        await quizService.submitQuiz(
          quizId,
          answers
        );

      setResult(data);
    } catch (err) {
      setError(
        getErrorMessage(
          err,
          "Unable to submit quiz."
        )
      );
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return (
      <LoadingSpinner text="Loading quiz..." />
    );
  }

  if (!quiz) {
    return (
      <div className="container py-5">
        <ErrorState
          message={
            error ||
            "Quiz could not be loaded."
          }
          onRetry={load}
        />
      </div>
    );
  }

  return (
    <div className="container py-5 quiz-container">
      {error && (
        <ErrorState message={error} />
      )}

      {!result ? (
        <>
          <h1>{quiz.title}</h1>

          <p className="text-secondary">
            {quiz.description}
          </p>

          <Quiz
            quiz={quiz}
            selectedAnswers={
              selectedAnswers
            }
            setSelectedAnswers={
              setSelectedAnswers
            }
            onSubmit={submit}
            submitting={
              submitting
            }
          />
        </>
      ) : (
        <div className="card shadow-sm text-center">
          <div className="card-body p-5">
            <h1>
              Quiz Complete
            </h1>

            <div className="display-4 fw-bold my-4">
              {result.score}%
            </div>

            <p>
              Correct Answers:{" "}
              {result.correct_answers} /{" "}
              {result.total_questions}
            </p>

            <Link
              to="/student/dashboard"
              className="btn btn-primary"
            >
              Back to Dashboard
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
