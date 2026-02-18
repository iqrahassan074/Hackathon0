import React, { useState, useEffect } from 'react';
import { settingsService } from '../../services/settings';
import { Button, Loading } from '../../components/shared';

/**
 * Settings Page
 * User preferences and configuration
 */
export default function Settings() {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({
    theme: 'light',
    notifications_enabled: true,
    ai_assistant_enabled: true,
    ai_provider: 'claude',
  });

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const data = await settingsService.get();
      setSettings(data);
      setFormData({
        theme: data.theme,
        notifications_enabled: data.notifications_enabled,
        ai_assistant_enabled: data.ai_assistant_enabled,
        ai_provider: data.ai_provider,
      });
    } catch (error) {
      console.error('Failed to load settings:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const updated = await settingsService.update(formData);
      setSettings(updated);
    } catch (error) {
      console.error('Failed to save settings:', error);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <Loading variant="overlay" text="Loading settings..." />;
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <header className="bg-white dark:bg-gray-800 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="h-16 flex items-center">
            <h1 className="text-xl font-bold text-gray-900 dark:text-white">Settings</h1>
          </div>
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Appearance */}
          <div className="card">
            <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
              Appearance
            </h2>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Theme
              </label>
              <select
                value={formData.theme}
                onChange={(e) => setFormData({ ...formData, theme: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg
                         focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
              >
                <option value="light">Light</option>
                <option value="dark">Dark</option>
                <option value="system">System</option>
              </select>
            </div>
          </div>

          {/* Notifications */}
          <div className="card">
            <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
              Notifications
            </h2>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={formData.notifications_enabled}
                onChange={(e) =>
                  setFormData({ ...formData, notifications_enabled: e.target.checked })
                }
                className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
              />
              <span className="ml-2 text-gray-700 dark:text-gray-300">
                Enable notifications
              </span>
            </label>
          </div>

          {/* AI Assistant */}
          <div className="card">
            <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
              AI Assistant
            </h2>
            <div className="space-y-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={formData.ai_assistant_enabled}
                  onChange={(e) =>
                    setFormData({ ...formData, ai_assistant_enabled: e.target.checked })
                  }
                  className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
                />
                <span className="ml-2 text-gray-700 dark:text-gray-300">
                  Enable AI assistant
                </span>
              </label>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  AI Provider
                </label>
                <select
                  value={formData.ai_provider}
                  onChange={(e) =>
                    setFormData({ ...formData, ai_provider: e.target.value })
                  }
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg
                           focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
                >
                  <option value="claude">Claude</option>
                  <option value="qwen">Qwen</option>
                </select>
              </div>
            </div>
          </div>

          <div className="flex justify-end">
            <Button type="submit" loading={saving}>
              Save Changes
            </Button>
          </div>
        </form>
      </main>
    </div>
  );
}
