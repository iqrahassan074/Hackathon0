import { useState, useCallback } from 'react';
import { useTaskStore } from '../store/taskStore';
import { taskService } from '../services/tasks';

/**
 * useTasks Hook
 * Custom hook for task operations
 */
export function useTasks() {
  const { addTask, updateTask, removeTask, setTasks } = useTaskStore();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchTasks = useCallback(async (params) => {
    setLoading(true);
    setError(null);
    try {
      const tasks = await taskService.getAll(params);
      setTasks(tasks);
      return tasks;
    } catch (err) {
      setError('Failed to fetch tasks');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [setTasks]);

  const createTask = useCallback(async (taskData) => {
    setLoading(true);
    setError(null);
    try {
      const task = await taskService.create(taskData);
      addTask(task);
      return task;
    } catch (err) {
      setError('Failed to create task');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [addTask]);

  const updateTaskById = useCallback(async (taskId, taskData) => {
    setLoading(true);
    setError(null);
    try {
      const task = await taskService.update(taskId, taskData);
      updateTask(task);
      return task;
    } catch (err) {
      setError('Failed to update task');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [updateTask]);

  const deleteTaskById = useCallback(async (taskId) => {
    setLoading(true);
    setError(null);
    try {
      await taskService.delete(taskId);
      removeTask(taskId);
    } catch (err) {
      setError('Failed to delete task');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [removeTask]);

  const completeTask = useCallback(async (taskId) => {
    setLoading(true);
    setError(null);
    try {
      const task = await taskService.markComplete(taskId);
      updateTask(task);
      return task;
    } catch (err) {
      setError('Failed to complete task');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [updateTask]);

  return {
    tasks: useTaskStore.getState().tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask: updateTaskById,
    deleteTask: deleteTaskById,
    completeTask,
  };
}
