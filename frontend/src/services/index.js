import api from './api';

/**
 * Settings Service
 * API calls for user settings
 */
export const settingsService = {
  /**
   * Get user settings
   */
  get: async () => {
    const response = await api.get('/settings/');
    return response.data;
  },

  /**
   * Update user settings
   */
  update: async (settingsData) => {
    const response = await api.put('/settings/', settingsData);
    return response.data;
  },
};

/**
 * AI Service
 * API calls for AI features
 */
export const aiService = {
  /**
   * Get task recommendations
   */
  getRecommendations: async (context = null, taskIds = null) => {
    const response = await api.post('/ai/recommend', { context, task_ids: taskIds });
    return response.data;
  },

  /**
   * Optimize a specific task
   */
  optimizeTask: async (taskId, focusAreas = null) => {
    const response = await api.post('/ai/optimize', {
      task_id: taskId,
      focus_areas: focusAreas,
    });
    return response.data;
  },

  /**
   * Get AI recommendation history
   */
  getHistory: async (limit = 50) => {
    const response = await api.get(`/ai/history?limit=${limit}`);
    return response.data;
  },

  /**
   * Accept a recommendation
   */
  acceptRecommendation: async (recommendationId) => {
    const response = await api.post(`/ai/history/${recommendationId}/accept`);
    return response.data;
  },
};
