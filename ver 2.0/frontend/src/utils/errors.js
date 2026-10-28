export function getErrorCode(error) {
  return error?.response?.data?.error || null;
}

export function getErrorMessage(
  error,
  fallback = "Something went wrong."
) {
  if (error?.code === "ECONNABORTED") {
    return "The request timed out. Please try again.";
  }

  if (error?.request && !error?.response) {
    return "Unable to connect to the server.";
  }

  return (
    error?.response?.data?.message ||
    error?.message ||
    fallback
  );
}

export function isAuthenticationError(error) {
  return error?.response?.status === 401;
}

export function isPermissionError(error) {
  return error?.response?.status === 403;
}
