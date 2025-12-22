// frontend/src/config/api.ts

// Get the API base URL from environment or use default
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const API_CONFIG = {
  baseUrl: API_BASE_URL,
  endpoints: {
    query: '/query',
    health: '/health',
    plans: '/plans',
  }
};

export default API_CONFIG;
