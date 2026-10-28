import api from "./api";

const enrollmentService = {
  async enroll(courseId) {
    const response = await api.post(
      `/courses/${courseId}/enroll`
    );
    return response.data.data;
  },

  async getMyCourses() {
    const response = await api.get(
      "/students/me/courses"
    );
    return response.data.data;
  },

  async completeLesson(lessonId) {
    const response = await api.post(
      `/lessons/${lessonId}/complete`
    );
    return response.data.data;
  },

  async getCourseProgress(courseId) {
    const response = await api.get(
      `/courses/${courseId}/progress`
    );
    return response.data.data;
  },
};

export default enrollmentService;
