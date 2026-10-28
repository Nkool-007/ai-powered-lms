import api from "./api";

const aiService = {
  async generateQuiz(payload) {
    const response = await api.post("/ai/generate-quiz", payload);
    return response.data.data;
  },

  async reindexCourse(courseId) {
    const response = await api.post(`/ai/courses/${courseId}/reindex`);
    return response.data.data;
  },

  async chat({ courseId, message, conversationId = null }) {
    const response = await api.post("/ai/chat", {
      course_id: courseId,
      message,
      conversation_id: conversationId,
    });
    return response.data.data;
  },

  async getConversations(courseId) {
    const response = await api.get("/ai/conversations", {
      params: courseId ? { course_id: courseId } : {},
    });
    return response.data.data;
  },

  async getConversation(conversationId) {
    const response = await api.get(`/ai/conversations/${conversationId}`);
    return response.data.data;
  },
};

export default aiService;
