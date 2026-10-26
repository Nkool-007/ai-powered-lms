export default function Button({ children, variant = "primary", loading = false, disabled = false, type = "button", className = "", ...props }) {
  return (
    <button type={type} disabled={disabled || loading} className={`btn btn-${variant} ${className}`} {...props}>
      {loading ? "Please wait..." : children}
    </button>
  );
}
