import axios from 'axios';

// Base URL - reads from environment variables
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,  // 30 second timeout
});

// Request interceptor - runs before every request
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor - runs after every response
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.config.url}`, response.data);
    return response;
  },
  (error) => {
    console.error('❌ Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// ==================== API FUNCTIONS ====================

/**
 * Get book recommendations based on query and filters
 * @param {string} query - Search query (e.g., "mystery book with twists")
 * @param {string} category - Book category (default: "All")
 * @param {string} tone - Emotional tone (default: "All")
 * @param {number} initialTopK - Initial results to fetch (default: 50)
 * @param {number} finalTopK - Final results to return (default: 16)
 * @returns {Promise} Response with books array and metadata
 */
export const getRecommendations = async (
  query, 
  category = 'All', 
  tone = 'All',
  initialTopK = 50,
  finalTopK = 16
) => {
  const response = await api.post('/api/recommendations', {
    query,
    category,
    tone,
    initial_top_k: initialTopK,
    final_top_k: finalTopK
  });
  return response.data;
};

/**
 * Get list of available book categories
 * @returns {Promise<string[]>} Array of category names
 */
export const getCategories = async () => {
  const response = await api.get('/api/categories');
  return response.data.categories;
};

/**
 * Get list of available emotional tones
 * @returns {Promise<string[]>} Array of tone names
 */
export const getTones = async () => {
  const response = await api.get('/api/tones');
  return response.data.tones;
};

/**
 * Health check endpoint
 * @returns {Promise} API health status
 */
export const checkHealth = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

// Export the configured axios instance for custom requests
export default api;
