import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-3xl font-bold text-gray-80 mb-4">Suno Prompt Generator</h1>
        <p className="text-lg text-gray-600">
          Create, manage, and optimize prompts for the Suno AI music generation platform
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <h2 className="text-xl font-semibold mb-4">Generate New Prompt</h2>
          <p className="text-gray-600 mb-4">
            Create custom music prompts with various parameters like genre, mood, style, instruments, and voice tags.
          </p>
          <Link 
            to="/prompt-generator" 
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Create Prompt
          </Link>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <h2 className="text-xl font-semibold mb-4">Template Library</h2>
          <p className="text-gray-600 mb-4">
            Browse and use pre-built prompt templates or create your own for consistent results.
          </p>
          <Link 
            to="/template-library" 
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-60 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Browse Templates
          </Link>
        </div>
     </div>
     
     <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
        <h2 className="text-xl font-semibold mb-4">About Suno Prompts</h2>
        <p className="text-gray-600 mb-4">
          Suno AI music generation platform allows you to create music from text prompts. 
          The quality of the output depends heavily on the quality of your prompts. 
          This tool helps you create effective prompts that combine genre, mood, style, instruments, 
          voice tags, and other parameters to generate the music you envision.
        </p>
        <p className="text-gray-600">
          Explore different combinations of elements to create unique and compelling music prompts.
        </p>
      </div>
    </div>
  );
};

export default Home;