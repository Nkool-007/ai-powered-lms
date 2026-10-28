import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

import authService from "../services/authService";
import authStorage from "../utils/authStorage";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(
    () => authStorage.getToken()
  );
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  function clearSession() {
    authStorage.clearToken();
    setToken(null);
    setUser(null);
  }

  useEffect(() => {
    function handleExpiredSession() {
      clearSession();
    }

    window.addEventListener(
      "smartlms:auth-expired",
      handleExpiredSession
    );

    return () => {
      window.removeEventListener(
        "smartlms:auth-expired",
        handleExpiredSession
      );
    };
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function restoreSession() {
      if (!token) {
        if (!cancelled) {
          setUser(null);
          setLoading(false);
        }
        return;
      }

      try {
        setLoading(true);

        const currentUser =
          await authService.getCurrentUser();

        if (!cancelled) {
          setUser(currentUser);
        }
      } catch {
        if (!cancelled) {
          clearSession();
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    restoreSession();

    return () => {
      cancelled = true;
    };
  }, [token]);

  async function login(credentials) {
    const result = await authService.login(
      credentials
    );

    authStorage.setToken(result.access_token);
    setToken(result.access_token);
    setUser(result.user);

    return result.user;
  }

  async function register(payload) {
    return authService.register(payload);
  }

  function logout() {
    clearSession();
  }

  const value = useMemo(
    () => ({
      token,
      user,
      loading,
      login,
      register,
      logout,
      isAuthenticated: Boolean(token && user),
    }),
    [token, user, loading]
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used inside AuthProvider"
    );
  }

  return context;
}
