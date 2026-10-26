import Button from "../common/Button";

export default function Quiz({ quiz, selectedAnswers, setSelectedAnswers, onSubmit, submitting }) {
  function choose(questionId, optionId) { setSelectedAnswers({ ...selectedAnswers, [questionId]: optionId }); }
  return (
    <form onSubmit={(event) => { event.preventDefault(); onSubmit(); }}>
      {quiz.questions.map((question, index) => (
        <section key={question.id} className="card mb-4"><div className="card-body">
          <h2 className="h5">Question {index + 1}</h2><p className="fw-semibold">{question.question}</p>
          {question.options.map((option) => (
            <div key={option.id} className="form-check mb-2"><input className="form-check-input" type="radio" name={`question-${question.id}`} id={`option-${option.id}`} checked={selectedAnswers[question.id] === option.id} onChange={() => choose(question.id, option.id)} /><label className="form-check-label" htmlFor={`option-${option.id}`}>{option.text}</label></div>
          ))}
        </div></section>
      ))}
      <Button type="submit" loading={submitting}>Submit Quiz</Button>
    </form>
  );
}
