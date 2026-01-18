import axios from 'axios';

const API_BASE_URLs = {
  auth: 'https://omnirouter-auth1.onrender.com',
  project: 'https://omnirouter-project-services.onrender.com',
  chat: 'https://omnirouter-chatservice.onrender.com'
};

// Create axios instances for each service
const authApi = axios.create({ 
  baseURL: API_BASE_URLs.auth,
  withCredentials: true
});
const projectApi = axios.create({ 
  baseURL: API_BASE_URLs.project,
  withCredentials: true
});
const chatApi = axios.create({ 
  baseURL: API_BASE_URLs.chat,
  withCredentials: true
});

// Add token to requests
const addTokenToRequest = (token) => {
  if (token) {
    authApi.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    projectApi.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    chatApi.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete authApi.defaults.headers.common['Authorization'];
    delete projectApi.defaults.headers.common['Authorization'];
    delete chatApi.defaults.headers.common['Authorization'];
  }
};

// Auth API
export const authAPI = {
  register: (email, password) =>
    authApi.post('/auth/register', { email, password }),
  login: (email, password) =>
    authApi.post('/auth/login', { email, password })
};

// Project API
export const projectAPI = {
  createProject: (name, description) =>
    projectApi.post('/projects', { name, description }),
  getProjects: () =>
    projectApi.get('/projects'),
  getProject: (projectId) =>
    projectApi.get(`/projects/${projectId}`),
  updateProject: (projectId, name, description) =>
    projectApi.put(`/projects/${projectId}`, { name, description }),
  deleteProject: (projectId) =>
    projectApi.delete(`/projects/${projectId}`),
  
  // Prompts
  createPrompt: (projectId, name, content) =>
    projectApi.post(`/projects/${projectId}/prompts`, { name, content }),
  getPrompts: (projectId) =>
    projectApi.get(`/projects/${projectId}/prompts`),
  updatePrompt: (projectId, promptId, name, content) =>
    projectApi.put(`/projects/${projectId}/prompts/${promptId}`, { name, content }),
  deletePrompt: (projectId, promptId) =>
    projectApi.delete(`/projects/${projectId}/prompts/${promptId}`)
};

// Chat API
export const chatAPI = {
  createConversation: (projectId) =>
    chatApi.post('/conversations', null, { params: { project_id: projectId } }),
  getConversation: (conversationId) =>
    chatApi.get(`/conversations/${conversationId}`),
  getConversationMessages: (conversationId) =>
    chatApi.get(`/conversations/${conversationId}/messages`),
  sendMessage: (conversationId, content) =>
    chatApi.post(`/conversations/${conversationId}/messages`, { content }),
  listProjectConversations: (projectId) =>
    chatApi.get(`/conversations/project/${projectId}`),
  deleteConversation: (conversationId) =>
    chatApi.delete(`/conversations/${conversationId}`)
};

// Token management
export const setAuthToken = (token) => {
  if (token) {
    localStorage.setItem('token', token);
    addTokenToRequest(token);
  }
};

export const getAuthToken = () => {
  return localStorage.getItem('token');
};

export const clearAuthToken = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  addTokenToRequest(null);
};

// Add request interceptor to ensure token is always added
const addTokenInterceptor = (config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
};

projectApi.interceptors.request.use(addTokenInterceptor);
chatApi.interceptors.request.use(addTokenInterceptor);
authApi.interceptors.request.use(addTokenInterceptor);

// Add response interceptor to handle 401 errors
const handle401 = (error) => {
  if (error.response?.status === 401) {
    // Token expired or invalid - clear auth and redirect to login
    clearAuthToken();
    window.location.href = '/login';
  }
  console.error('API Error:', {
    url: error.config?.url,
    method: error.config?.method,
    status: error.response?.status,
    data: error.response?.data,
    message: error.message
  });
  return Promise.reject(error);
};

projectApi.interceptors.response.use(response => response, handle401);
chatApi.interceptors.response.use(response => response, handle401);
authApi.interceptors.response.use(response => response, handle401);

// Initialize with stored token
const storedToken = getAuthToken();
if (storedToken) {
  addTokenToRequest(storedToken);
}
