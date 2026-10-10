import axios from 'axios';

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 30000,
});

// Attach token
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('pp_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Handle 401
API.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('pp_token');
      localStorage.removeItem('pp_user');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

export default API;

// Auth
export const authAPI = {
  register: (data) => API.post('/api/auth/register', data),
  login: (data) => API.post('/api/auth/login', data),
  me: () => API.get('/api/auth/me'),
};

// Student
export const studentAPI = {
  getProfile: () => API.get('/api/student/profile'),
  updateProfile: (data) => API.put('/api/student/profile', data),
  getDashboard: () => API.get('/api/student/dashboard-summary'),
};

// Job Roles
export const jobRolesAPI = {
  list: () => API.get('/api/job-roles'),
  get: (id) => API.get(`/api/job-roles/${id}`),
  create: (data) => API.post('/api/job-roles', data),
  update: (id, data) => API.put(`/api/job-roles/${id}`, data),
};

// Assessments
export const assessmentAPI = {
  getQuestions: (type, count = 15) => API.get(`/api/assessments/questions/${type}?count=${count}`),
  submit: (data) => API.post('/api/assessments/submit', data),
  getHistory: (type) => API.get(`/api/assessments/history${type ? `?assessment_type=${type}` : ''}`),
};

// Readiness
export const readinessAPI = {
  calculate: (job_role_id) => API.post('/api/readiness/calculate', { job_role_id }),
  getCurrent: (roleId) => API.get(`/api/readiness/current${roleId ? `?job_role_id=${roleId}` : ''}`),
  getHistory: () => API.get('/api/readiness/history'),
  getSkillGaps: (roleId) => API.get(`/api/readiness/skill-gaps${roleId ? `?job_role_id=${roleId}` : ''}`),
};

// Interview
export const interviewAPI = {
  start: (job_role_id) => API.post('/api/interview/start', { job_role_id }),
  evaluate: (data) => API.post('/api/interview/evaluate', data),
  complete: (id) => API.post(`/api/interview/complete/${id}`),
  getHistory: () => API.get('/api/interview/history'),
};

// Resume
export const resumeAPI = {
  analyze: (formData) => API.post('/api/resume/analyze', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  getHistory: () => API.get('/api/resume/history'),
};

// LeetCode
export const leetcodeAPI = {
  getProgress: () => API.get('/api/leetcode/progress'),
  update: (data) => API.post('/api/leetcode/update', data),
};

// Recommendations
export const recAPI = {
  get: (roleId) => API.get(`/api/recommendations${roleId ? `?job_role_id=${roleId}` : ''}`),
};

// Admin
export const adminAPI = {
  getDashboard: () => API.get('/api/admin/dashboard'),
  getStudents: (params) => API.get('/api/admin/students', { params }),
  getStudent: (id) => API.get(`/api/admin/students/${id}`),
  getSkillGaps: () => API.get('/api/admin/skill-gaps'),
  getAnalytics: () => API.get('/api/admin/analytics'),
  getModelEval: () => API.get('/api/admin/model-evaluation'),
};
