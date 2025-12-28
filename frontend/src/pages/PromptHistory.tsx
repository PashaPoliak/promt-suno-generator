import React, { useState, useEffect } from 'react';
import { getPrompts, deletePrompt } from '../services/api';
import { PromptResponse } from '../types';

const PromptHistory: React.FC = () => {
  const [prompts, setPrompts] = useState<PromptResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPrompts();
  }, []);

  const fetchPrompts = async () => {
    try {
      setLoading(true);
      const response = await getPrompts();
      setPrompts(response);
    } catch (err) {
      setError('Failed to fetch prompts');
      console.error('Error fetching prompts:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this prompt?')) {
      try {
        await deletePrompt(id);
        fetchPrompts();
      } catch (err) {
        setError('Failed to delete prompt');
        console.error('Error deleting prompt:', err);
      }
    }
 };

  if (loading) return <div className="text-center py-8">Loading prompts...</div>;
  if (error) return <div className="text-center py-8 text-red-600">{error}</div>;

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Prompt History</h1>
      
      <div className="space-y-6">
        {prompts.map(prompt => (
          <div key={prompt.id} className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Generated Prompt
                  </label>
                  <div className="p-4 bg-gray-50 rounded border border-gray-300">
                    <p className="text-gray-800">{prompt.prompt_text}</p>
                  </div>
                </div>
                
                {prompt.parameters && Object.keys(prompt.parameters).length > 0 && (
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Parameters
                    </label>
                    <div className="p-4 bg-gray-50 rounded border border-gray-300">
                      <pre className="text-sm text-gray-800">
                        {JSON.stringify(prompt.parameters, null, 2)}
                      </pre>
                    </div>
                  </div>
                )}
                
                <div className="text-sm text-gray-500">
                  Created: {new Date(prompt.created_at).toLocaleString()}
                </div>
              </div>
              <button
                onClick={() => handleDelete(prompt.id)}
                className="ml-4 text-red-600 hover:text-red-900"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
      
      {prompts.length === 0 && (
        <div className="text-center py-8 text-gray-50">
          No prompts found. Generate some prompts to see them here.
        </div>
      )}
    </div>
  );
};

export default PromptHistory;