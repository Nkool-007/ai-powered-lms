import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import aiService from "../../services/aiService";
import courseService from "../../services/courseService";
import quizService from "../../services/quizService";
import { getErrorMessage } from "../../utils/errors";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import ErrorState from "../../components/common/ErrorState";


export default function AIQuizGenerator() {
  const { courseId, lessonId } = useParams();
  const navigate = useNavigate();

  const [lesson, setLesson] = useState(null);
  const [difficulty, setDifficulty] = useState("medium");
  const [numberOfQuestions, setNumberOfQuestions] = useState(5);
  const [draft, setDraft] = useState(null);
  const [quizTitle, setQuizTitle] = useState("");
  const [loadingLesson, setLoadingLesson] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    courseService
      .getLesson(lessonId)
      .then((result) => {
        setLesson(result);
        setQuizTitle(`${result.title} Quiz`);
      })
      .catch((err) => {
        setError(getErrorMessage(err, "Could not load Lesson."));
      })
      .finally(() => setLoadingLesson(false));
  }, [lessonId]);

  async function generate() {
    try {
      setGenerating(true);
      setError("");
      setDraft(null);

      const result = await aiService.generateQuiz({
        lesson_id: Number(lessonId),
        difficulty,
        number_of_questions: Number(numberOfQuestions),
      });

      setDraft(result);
    } catch (err) {
      setError(getErrorMessage(err, "Quiz generation failed."));
    } finally {
      setGenerating(false);
    }
  }

  function updateQuestion(questionIndex, field, value) {
    setDraft((current) => ({
      ...current,
      questions: current.questions.map((question, index) =>
        index === questionIndex ? { ...question, [field]: value } : question
      ),
    }));
  }

  function updateOption(questionIndex, optionIndex, value) {
    setDraft((current) => ({
      ...current,
      questions: current.questions.map((question, index) => {
        if (index !== questionIndex) return question;
        const options = [...question.options];
        options[optionIndex] = value;
        return { ...question, options };
      }),
    }));
  }

  function removeQuestion(questionIndex) {
    setDraft((current) => ({
      ...current,
      questions: current.questions.filter((_, index) => index !== questionIndex),
    }));
  }

  async function approveAndSave() {
    if (!draft || draft.questions.length === 0) return;

    try {
      setSaving(true);
      setError("");

      const payload = {
        title: quizTitle,
        description: `Instructor-reviewed Quiz generated from Lesson: ${draft.lesson_title}`,
        questions: draft.questions.map((question, questionIndex) => ({
          question_text: question.question,
          position: questionIndex + 1,
          options: question.options.map((option, optionIndex) => ({
            option_text: option,
            position: optionIndex + 1,
            is_correct: optionIndex === Number(question.correct_answer),
          })),
        })),
      };

      const quiz = await quizService.createQuiz(draft.course_id, payload);

      navigate(`/instructor/courses/${draft.course_id}/quiz`, {
        state: { createdQuizId: quiz.id },
      });
    } catch (err) {
      setError(getErrorMessage(err, "Could not save Quiz."));
    } finally {
      setSaving(false);
    }
  }

  if (loadingLesson) {
    return <LoadingSpinner text="Loading Lesson..." />;
  }

  return (
    <div className="container py-4">
      <h1 className="h2">AI Quiz Generator</h1>
      <p className="text-secondary">Lesson: {lesson?.title}</p>

      {error && <ErrorState message={error} />}

      <div className="card mb-4">
        <div className="card-body">
          <label className="form-label">Difficulty</label>
          <select
            className="form-select mb-3"
            value={difficulty}
            onChange={(event) => setDifficulty(event.target.value)}
          >
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>

          <label className="form-label">Number of Questions</label>
          <input
            className="form-control mb-3"
            type="number"
            min="1"
            max="10"
            value={numberOfQuestions}
            onChange={(event) => setNumberOfQuestions(event.target.value)}
          />

          <button className="btn btn-primary" onClick={generate} disabled={generating}>
            {generating ? "Generating..." : "Generate Quiz With AI"}
          </button>
        </div>
      </div>

      {draft && (
        <>
          <div className="mb-4">
            <label className="form-label">Quiz Title</label>
            <input
              className="form-control"
              value={quizTitle}
              onChange={(event) => setQuizTitle(event.target.value)}
            />
          </div>

          {draft.questions.map((question, questionIndex) => (
            <div className="card mb-4" key={questionIndex}>
              <div className="card-body">
                <h2 className="h5">Question {questionIndex + 1}</h2>

                <textarea
                  className="form-control mb-3"
                  value={question.question}
                  onChange={(event) =>
                    updateQuestion(questionIndex, "question", event.target.value)
                  }
                />

                {question.options.map((option, optionIndex) => (
                  <div className="input-group mb-2" key={optionIndex}>
                    <div className="input-group-text">
                      <input
                        type="radio"
                        name={`correct-${questionIndex}`}
                        checked={Number(question.correct_answer) === optionIndex}
                        onChange={() =>
                          updateQuestion(questionIndex, "correct_answer", optionIndex)
                        }
                      />
                    </div>

                    <input
                      className="form-control"
                      value={option}
                      onChange={(event) =>
                        updateOption(questionIndex, optionIndex, event.target.value)
                      }
                    />
                  </div>
                ))}

                <label className="form-label mt-3">Explanation</label>
                <textarea
                  className="form-control mb-3"
                  value={question.explanation}
                  onChange={(event) =>
                    updateQuestion(questionIndex, "explanation", event.target.value)
                  }
                />

                <button
                  className="btn btn-outline-danger btn-sm"
                  onClick={() => removeQuestion(questionIndex)}
                >
                  Remove Question
                </button>
              </div>
            </div>
          ))}

          <div className="d-flex gap-2">
            <button
              className="btn btn-success"
              disabled={saving}
              onClick={approveAndSave}
            >
              {saving ? "Saving..." : "Approve & Save Quiz"}
            </button>

            <button
              className="btn btn-outline-secondary"
              onClick={() => setDraft(null)}
            >
              Reject Generation
            </button>
          </div>
        </>
      )}
    </div>
  );
}
