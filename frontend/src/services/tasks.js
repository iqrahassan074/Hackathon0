import api from './api';

/**
 * Task Service
 * API calls for task management
 */
export const taskService = {
  /**
   * Create a new task
   */
  create: async (taskData) => {
    const response = await api.post('/tasks/', taskData);
    return response.data;
  },

  /**
   * Get all tasks with optional filters
   */
  getAll: async (params = {}) => {
    const response = await api.get('/tasks/', { params });
    return response.data;
  },

  /**
   * Get task statistics
   */
  getStats: async () => {
    const response = await api.get('/tasks/stats');
    return response.data;
  },

  /**
   * Get a specific task by ID
   */
  getById: async (taskId) => {
    const response = await api.get(`/tasks/${taskId}`);
    return response.data;
  },

  /**
   * Update a task
   */
  update: async (taskId, taskData) => {
    const response = await api.put(`/tasks/${taskId}`, taskData);
    return response.data;
  },

  /**
   * Delete a task
   */
  delete: async (taskId) => {
    await api.delete(`/tasks/${taskId}`);
  },

  /**
   * Mark a task as complete
   */
  markComplete: async (taskId) => {
    const response = await api.patch(`/tasks/${taskId}/complete`);
    return response.data;
  },
};
