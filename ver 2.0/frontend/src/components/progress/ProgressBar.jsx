export default function ProgressBar({
  percentage = 0,
}) {
  const safeValue = Math.min(
    100,
    Math.max(0, Number(percentage) || 0)
  );

  return (
    <div>
      <div className="d-flex justify-content-between mb-1">
        <span>Progress</span>
        <strong>{safeValue}%</strong>
      </div>

      <div
        className="progress"
        role="progressbar"
        aria-valuenow={safeValue}
        aria-valuemin="0"
        aria-valuemax="100"
      >
        <div
          className="progress-bar"
          style={{ width: `${safeValue}%` }}
        />
      </div>
    </div>
  );
}
