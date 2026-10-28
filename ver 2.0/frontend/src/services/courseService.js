import api from "./api";

const courseService = {
  async getCourses() {
    const response = await api.get("/courses");
    return response.data.data;
  },

  async getCourse(courseId) {
    const response = await api.get(
      `/courses/${courseId}`
    );
    return response.data.data;
  },

  async getInstructorCourses() {
    const response = await api.get(
      "/instructor/courses"
    );
    return response.data.data;
  },

  async createCourse(payload) {
    const response = await api.post(
      "/courses",
      payload
    );
    return response.data.data;
  },

  async updateCourse(courseId, payload) {
    const response = await api.put(
      `/courses/${courseId}`,
      payload
    );
    return response.data.data;
  },

  async deleteCourse(courseId) {
    const response = await api.delete(
      `/courses/${courseId}`
    );
    return response.data.data;
  },

  async publishCourse(courseId) {
    const response = await api.patch(
      `/courses/${courseId}/publish`
    );
    return response.data.data;
  },

  async getModules(courseId) {
    const response = await api.get(
      `/courses/${courseId}/modules`
    );
    return response.data.data;
  },

  async createModule(courseId, payload) {
    const response = await api.post(
      `/courses/${courseId}/modules`,
      payload
    );
    return response.data.data;
  },

  async updateModule(moduleId, payload) {
    const response = await api.put(
      `/modules/${moduleId}`,
      payload
    );
    return response.data.data;
  },

  async deleteModule(moduleId) {
    const response = await api.delete(
      `/modules/${moduleId}`
    );
    return response.data.data;
  },

  async getLessons(moduleId) {
    const response = await api.get(
      `/modules/${moduleId}/lessons`
    );
    return response.data.data;
  },

  async getLesson(lessonId) {
    const response = await api.get(
      `/lessons/${lessonId}`
    );
    return response.data.data;
  },

  async createLesson(moduleId, payload) {
    const response = await api.post(
      `/modules/${moduleId}/lessons`,
      payload
    );
    return response.data.data;
  },

  async updateLesson(lessonId, payload) {
    const response = await api.put(
      `/lessons/${lessonId}`,
      payload
    );
    return response.data.data;
  },

  async deleteLesson(lessonId) {
    const response = await api.delete(
      `/lessons/${lessonId}`
    );
    return response.data.data;
  },

  async getCourseOutline(courseId) {
    const modules = await this.getModules(courseId);

    return Promise.all(
      modules.map(async (module) => ({
        ...module,
        lessons: await this.getLessons(module.id),
      }))
    );
  },

  async getCourseStudents(courseId) {
    const response = await api.get(
      `/courses/${courseId}/students`
    );
    return response.data.data;
  },

  async getStudentProgress(courseId, studentId) {
    const response = await api.get(
      `/courses/${courseId}/students/${studentId}/progress`
    );
    return response.data.data;
  },
};

export default courseService;
