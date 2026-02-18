import React, { useState, useEffect } from 'react';
import { aiService } from '../../services/ai';
import { Button, Input, Loading } from '../../components/shared';

/**
 * AIPanel Component
 * AI assistant for task recommendations
 */
export default function AIPanel() {
  const [query, setQuery] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const getRecommendations = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await aiService.getRecommendations(query || null);
      setRecommendations(response.recommendations);
    } catch (err) {
      setError('AI service unavailable. Please try again later.');
      // Show fallback recommendations
      setRecommendations([
        'Review your pending tasks and prioritize by deadline',
        'Break large tasks into smaller, actionable steps',
        'Set specific due dates for better time management',
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleAccept = async (index) => {
    // In a full implementation, this would call the API to mark as accepted
    setRecommendations(recommendations.filter((_, i) => i !== index));
  };

  return (
    <div className="card h-full">
      <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white flex items-center">
        <svg className="w-5 h-5 mr-2 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
        AI Assistant
      </h2>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Ask for recommendations
          </label>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="E.g., Help me prioritize my tasks..."
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg
                     focus:ring-2 focus:ring-primary-500 focus:border-transparent
                     dark:bg-gray-700 dark:text-white resize-none"
            rows={3}
          />
        </div>

        <Button onClick={getRecommendations} loading={loading} className="w-full">
          Get Recommendations
        </Button>

        {error && (
          <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
        )}

        {recommendations.length > 0 && (
          <div className="space-y-3 pt-4 border-t border-gray-200 dark:border-gray-700">
            <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Recommendations
            </h3>
            {recommendations.map((rec, index) => (
              <div
                key={index}
                className="p-3 bg-primary-50 dark:bg-primary-900/20 rounded-lg"
              >
                <p className="text-sm text-gray-700 dark:text-gray-300">{rec}</p>
                <button
                  onClick={() => handleAccept(index)}
                  className="mt-2 text-xs text-primary-600 hover:text-primary-700 font-medium"
                >
                  ✓ Mark as done
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
