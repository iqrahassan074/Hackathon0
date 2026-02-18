import { create } from 'zustand';

/**
 * Task Store
 * Manages task state
 */
export const useTaskStore = create((set, get) => ({
  tasks: [],
  currentTask: null,
  stats: null,
  loading: false,
  error: null,

  setTasks: (tasks) => set({ tasks }),
  
  addTask: (task) =>
    set((state) => ({
      tasks: [task, ...state.tasks],
    })),

  updateTask: (updatedTask) =>
    set((state) => ({
      tasks: state.tasks.map((task) =>
        task.id === updatedTask.id ? updatedTask : task
      ),
      currentTask: state.currentTask?.id === updatedTask.id ? updatedTask : state.currentTask,
    })),

  removeTask: (taskId) =>
    set((state) => ({
      tasks: state.tasks.filter((task) => task.id !== taskId),
    })),

  setCurrentTask: (task) => set({ currentTask: task }),

  setStats: (stats) => set({ stats }),

  setLoading: (loading) => set({ loading }),

  setError: (error) => set({ error }),

  clearError: () => set({ error: null }),
}));
