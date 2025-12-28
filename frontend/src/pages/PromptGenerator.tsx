import React, { useState } from 'react';
import PromptForm from '../components/PromptGenerator/PromptForm';
import { GenerateRequest, GenerateResponse } from '../types';
import { generatePrompt } from '../services/api';

const PromptGenerator: React.FC = () => {
  const [generatedPrompt, setGeneratedPrompt] = useState<GenerateResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: GenerateRequest) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await generatePrompt(data);
      setGeneratedPrompt(response);
    } catch (err) {
      setError('Failed to generate prompt. Please try again.');
      console.error('Error generating prompt:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Generate Music Prompt</h1>
      
      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200 mb-8">
        <h2 className="text-lg font-semibold mb-4">Create New Prompt</h2>
        <PromptForm onSubmit={handleSubmit} />
      </div>

      {isLoading && (
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <p className="text-gray-600">Generating your prompt...</p>
        </div>
      )}

      {error && (
        <div className="bg-red-50 p-6 rounded-lg border border-red-200">
          <p className="text-red-600">{error}</p>
        </div>
      )}

      {generatedPrompt && !isLoading && (
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <h2 className="text-lg font-semibold mb-4">Generated Prompt</h2>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Prompt Text
            </label>
            <div className="p-4 bg-gray-50 rounded border border-gray-300">
              <p className="text-gray-800">{generatedPrompt.prompt_text}</p>
            </div>
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Parameters Used
            </label>
            <div className="p-4 bg-gray-50 rounded border border-gray-300">
              <pre className="text-sm text-gray-800">
                {JSON.stringify(generatedPrompt.parameters_used, null, 2)}
              </pre>
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-70 mb-1">
              Validation Result
            </label>
            <div className="p-4 bg-gray-50 rounded border border-gray-300">
              <pre className="text-sm text-gray-800">
                {JSON.stringify(generatedPrompt.validation_result, null, 2)}
              </pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PromptGenerator;