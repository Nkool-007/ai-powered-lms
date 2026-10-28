export default function LoadingSpinner({
  text = "Loading...",
}) {
  return (
    <div
      className="d-flex flex-column align-items-center justify-content-center py-5"
      role="status"
      aria-live="polite"
    >
      <div className="spinner-border mb-3" />
      <p className="text-secondary mb-0">
        {text}
      </p>
    </div>
  );
}
