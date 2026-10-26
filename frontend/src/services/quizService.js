import api from "./api";

const quizService = {
  async createQuiz(courseId, payload) {
    const response = await api.post(`/courses/${courseId}/quizzes`, payload);
    return response.data.data;
  },
  async getQuiz(quizId) {
    const response = await api.get(`/quizzes/${quizId}`);
    return response.data.data;
  },
  async submitQuiz(quizId, answers) {
    const response = await api.post(`/quizzes/${quizId}/submit`, { answers });
    return response.data.data;
  },
  async getMyAttempts(courseId) {
    const response = await api.get("/students/me/quiz-attempts", {
      params: courseId ? { course_id: courseId } : {},
    });
    return response.data.data;
  },
};

export default quizService;
