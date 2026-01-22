import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 10000,
});

// Add request interceptor for debugging
apiClient.interceptors.request.use(
  config => {
    console.log(`🔵 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  error => Promise.reject(error)
);

// Add response interceptor for debugging
apiClient.interceptors.response.use(
  response => {
    console.log(`🟢 API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  error => {
    console.error(`🔴 API Error: ${error.config?.url}`, error.message);
    return Promise.reject(error);
  }
);

export const monitoringAPI = {
  // Pain Monitoring
  getPainStatus: async () => {
    const response = await apiClient.get('/pain/status');
    return response.data;
  },

  getPainHistory: async (limit = 100) => {
    const response = await apiClient.get(`/pain/history?limit=${limit}`);
    return response.data;
  },

  // Agitation Monitoring
  getAgitationStatus: async () => {
    const response = await apiClient.get('/agitation/status');
    return response.data;
  },

  getAgitationHistory: async (limit = 100) => {
    const response = await apiClient.get(`/agitation/history?limit=${limit}`);
    return response.data;
  },

  // Audio Monitoring
  getAudioStatus: async () => {
    const response = await apiClient.get('/audio/status');
    return response.data;
  },

  getAudioHistory: async (limit = 100) => {
    const response = await apiClient.get(`/audio/history?limit=${limit}`);
    return response.data;
  },

  // Alerts
  getAllAlerts: async (limit = 50) => {
    const response = await apiClient.get(`/alerts?limit=${limit}`);
    return response.data;
  },

  getCriticalAlerts: async () => {
    const response = await apiClient.get('/alerts/critical');
    return response.data;
  },

  acknowledgeAlert: async (alertId) => {
    const response = await apiClient.post(`/alerts/${alertId}/acknowledge`);
    return response.data;
  },

  // System Status
  getSystemStatus: async () => {
    const response = await apiClient.get('/system/status');
    return response.data;
  },

  startMonitoring: async (type) => {
    const response = await apiClient.post(`/monitoring/${type}/start`);
    return response.data;
  },

  stopMonitoring: async (type) => {
    const response = await apiClient.post(`/monitoring/${type}/stop`);
    return response.data;
  },

  // Health Check
  healthCheck: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

export default apiClient;
