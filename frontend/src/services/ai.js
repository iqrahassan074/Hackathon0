import api from './api';

/**
 * AI Service
 * API calls for AI recommendations and insights
 */
export const aiService = {
  /**
   * Get task recommendations from AI
   * @param {string|null} context - Optional context for recommendations
   * @returns {Promise<{recommendations: string[], message: string}>}
   */
  getRecommendations: async (context = null) => {
    const response = await api.post('/ai/recommend', { context });
    return response.data;
  },

  /**
   * Get AI optimization suggestions for a task
   * @param {string} taskId - Task ID
   * @param {string[]} focusAreas - Optional focus areas
   * @returns {Promise<object>}
   */
  optimizeTask: async (taskId, focusAreas = null) => {
    const response = await api.post('/ai/optimize', { task_id: taskId, focus_areas: focusAreas });
    return response.data;
  },

  /**
   * Get AI recommendation history
   * @param {number} limit - Max records to return
   * @returns {Promise<Array>}
   */
  getHistory: async (limit = 50) => {
    const response = await api.get(`/ai/history?limit=${limit}`);
    return response.data;
  },

  /**
   * Mark a recommendation as accepted
   * @param {string} recommendationId - Recommendation ID
   * @returns {Promise<object>}
   */
  acceptRecommendation: async (recommendationId) => {
    const response = await api.post(`/ai/history/${recommendationId}/accept`);
    return response.data;
  },
};
