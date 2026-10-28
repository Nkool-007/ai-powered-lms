import api from "./api";

const authService = {
  async register(payload) {
    const response = await api.post(
      "/auth/register",
      payload
    );

    return response.data.data;
  },

  async login(credentials) {
    const response = await api.post(
      "/auth/login",
      credentials
    );

    return response.data.data;
  },

  async getCurrentUser() {
    const response = await api.get("/auth/me");

    return response.data.data;
  },
};

export default authService;
