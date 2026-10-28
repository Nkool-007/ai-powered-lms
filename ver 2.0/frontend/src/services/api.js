import axios from "axios";

import authStorage from "../utils/authStorage";

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_BASE_URL ||
    "http://localhost:5000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
});

api.interceptors.request.use(
  (config) => {
    const token = authStorage.getToken();

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status;

    // Failed login requests also return 401. Only expire the session
    // when a token already existed.
    if (status === 401 && authStorage.hasToken()) {
      const code =
        error?.response?.data?.error ||
        "AUTHENTICATION_REQUIRED";

      authStorage.clearToken();

      window.dispatchEvent(
        new CustomEvent("smartlms:auth-expired", {
          detail: { code },
        })
      );
    }

    return Promise.reject(error);
  }
);

export default api;
