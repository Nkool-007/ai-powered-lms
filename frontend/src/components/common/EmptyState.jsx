export default function EmptyState({ title, message, action }) {
  return (
    <div className="empty-state text-center p-5">
      <h3>{title}</h3>
      <p className="text-secondary">{message}</p>
      {action}
    </div>
  );
}
