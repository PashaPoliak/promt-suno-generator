import React, { useState, useEffect } from 'react';
import { getAllCategories, getSingleCategory, createCategory, updateCategory, deleteCategory } from '../../services/api';
import { getAllTags, getSingleTag, createTag, updateTag, deleteTag } from '../../services/api';
import { getAllTemplates, getSingleTemplate, createTemplate, updateTemplate, deleteTemplate } from '../../services/api';
import { getPrompts, getPrompt, createPrompt, deletePrompt, combinePrompts, extendPrompt } from '../../services/api';

const ApiExplorer: React.FC = () => {
  const [endpoints, setEndpoints] = useState<any[]>([]);
  const [selectedEndpoint, setSelectedEndpoint] = useState<any>(null);
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // Define all endpoints
  useEffect(() => {
    const allEndpoints = [
      // Health and Status
      { id: 'health', name: 'Health Check', path: '/system/health', method: 'GET', apiFunction: () => fetch('/api/v1/system/health') },
      { id: 'status', name: 'System Status', path: '/system/status', method: 'GET', apiFunction: () => fetch('/api/v1/system/status') },
      
      // Playlist endpoints
      { id: 'v1-playlists', name: 'V1 Playlists', path: '/playlist/', method: 'GET', apiFunction: async () => fetch('/api/v1/playlist/') },
      { id: 'v1-playlist-id', name: 'V1 Playlist by ID', path: '/playlist/{id}', method: 'GET', apiFunction: async (id: string) => fetch(`/api/v1/playlist/${id}`) },
      
      // User endpoints
      { id: 'v1-users', name: 'V1 Users', path: '/users/', method: 'GET', apiFunction: async () => fetch('/api/v1/users/') },
      { id: 'v1-user-id', name: 'V1 User by ID', path: '/users/{id}', method: 'GET', apiFunction: async (id: string) => fetch(`/api/v1/users/${id}`) },
      
      // Profile endpoints
      { id: 'v1-profiles', name: 'V1 Profiles', path: '/profiles/', method: 'GET', apiFunction: async () => fetch('/api/v1/profiles/') },
      { id: 'v1-profile-id', name: 'V1 Profile by ID', path: '/profiles/{id}', method: 'GET', apiFunction: async (id: string) => fetch(`/api/v1/profiles/${id}`) },
      
      // Clip endpoints
      { id: 'v1-clips', name: 'V1 Clips', path: '/clip/', method: 'GET', apiFunction: async () => fetch('/api/v1/clip/') },
      { id: 'v1-clip-id', name: 'V1 Clip by ID', path: '/clip/{id}', method: 'GET', apiFunction: async (id: string) => fetch(`/api/v1/clip/${id}`) },
      { id: 'v1-clip-delete', name: 'V1 Delete Clip', path: '/clip/{id}', method: 'DELETE', apiFunction: async (id: string) => fetch(`/api/v1/clip/${id}`, { method: 'DELETE' }) },
      
      // Category endpoints
      { id: 'v1-categories', name: 'V1 Categories', path: '/categories/', method: 'GET', apiFunction: getAllCategories },
      { id: 'v1-category-id', name: 'V1 Category by ID', path: '/categories/{id}', method: 'GET', apiFunction: getSingleCategory },
      { id: 'v1-category-create', name: 'V1 Create Category', path: '/categories/', method: 'POST', apiFunction: createCategory },
      { id: 'v1-category-update', name: 'V1 Update Category', path: '/categories/{id}', method: 'PUT', apiFunction: updateCategory },
      { id: 'v1-category-delete', name: 'V1 Delete Category', path: '/categories/{id}', method: 'DELETE', apiFunction: deleteCategory },
      
      // Tag endpoints
      { id: 'v1-tags', name: 'V1 Tags', path: '/tags/', method: 'GET', apiFunction: getAllTags },
      { id: 'v1-tag-id', name: 'V1 Tag by ID', path: '/tags/{id}', method: 'GET', apiFunction: getSingleTag },
      { id: 'v1-tag-create', name: 'V1 Create Tag', path: '/tags/', method: 'POST', apiFunction: createTag },
      { id: 'v1-tag-update', name: 'V1 Update Tag', path: '/tags/{id}', method: 'PUT', apiFunction: updateTag },
      { id: 'v1-tag-delete', name: 'V1 Delete Tag', path: '/tags/{id}', method: 'DELETE', apiFunction: deleteTag },
      
      // Template endpoints
      { id: 'v1-templates', name: 'V1 Templates', path: '/templates/', method: 'GET', apiFunction: getAllTemplates },
      { id: 'v1-template-id', name: 'V1 Template by ID', path: '/templates/{id}', method: 'GET', apiFunction: getSingleTemplate },
      { id: 'v1-template-create', name: 'V1 Create Template', path: '/templates/', method: 'POST', apiFunction: createTemplate },
      { id: 'v1-template-update', name: 'V1 Update Template', path: '/templates/{id}', method: 'PUT', apiFunction: updateTemplate },
      { id: 'v1-template-delete', name: 'V1 Delete Template', path: '/templates/{id}', method: 'DELETE', apiFunction: deleteTemplate },
      
      // Prompt endpoints
      { id: 'v1-prompts', name: 'V1 Prompts', path: '/prompts/', method: 'GET', apiFunction: getPrompts },
      { id: 'v1-prompt-id', name: 'V1 Prompt by ID', path: '/prompts/{id}', method: 'GET', apiFunction: getPrompt },
      { id: 'v1-prompt-create', name: 'V1 Create Prompt', path: '/prompts/', method: 'POST', apiFunction: createPrompt },
      { id: 'v1-prompt-delete', name: 'V1 Delete Prompt', path: '/prompts/{id}', method: 'DELETE', apiFunction: deletePrompt },
      { id: 'v1-prompt-combine', name: 'V1 Combine Prompts', path: '/prompts/combine', method: 'POST', apiFunction: combinePrompts },
      { id: 'v1-prompt-extend', name: 'V1 Extend Prompt', path: '/prompts/extend', method: 'POST', apiFunction: extendPrompt },
      
      // V2 endpoints (JSON-based)
      { id: 'v2-playlists', name: 'V2 Playlists', path: '/playlist/', method: 'GET', apiFunction: async () => fetch('/api/v2/playlist/') },
      { id: 'v2-playlist-id', name: 'V2 Playlist by ID', path: '/playlist/{id}', method: 'GET', apiFunction: async (id: string) => fetch(`/api/v2/playlist/${id}`) },
      { id: 'v2-users', name: 'V2 Users', path: '/users/', method: 'GET', apiFunction: async () => fetch('/api/v2/users/') },
      { id: 'v2-user-id', name: 'V2 User by ID', path: '/users/{id}', method: 'GET', apiFunction: async (id: string) => fetch(`/api/v2/users/${id}`) },
      { id: 'v2-profiles', name: 'V2 Profiles', path: '/profiles/', method: 'GET', apiFunction: async () => fetch('/api/v2/profiles/') },
      { id: 'v2-profile-id', name: 'V2 Profile by ID', path: '/profiles/{id}', method: 'GET', apiFunction: async (id: string) => fetch(`/api/v2/profiles/${id}`) },
      { id: 'v2-clips', name: 'V2 Clips', path: '/clip/', method: 'GET', apiFunction: async () => fetch('/api/v2/clip/') },
      { id: 'v2-clip-id', name: 'V2 Clip by ID', path: '/clip/{id}', method: 'GET', apiFunction: async (id: string) => fetch(`/api/v2/clip/${id}`) },
      { id: 'v2-categories', name: 'V2 Categories', path: '/categories/', method: 'GET', apiFunction: async () => fetch('/api/v2/categories/') },
      { id: 'v2-tags', name: 'V2 Tags', path: '/tags/', method: 'GET', apiFunction: async () => fetch('/api/v2/tags/') },
      { id: 'v2-templates', name: 'V2 Templates', path: '/templates/', method: 'GET', apiFunction: async () => fetch('/api/v2/templates/') },
      { id: 'v2-prompts', name: 'V2 Prompts', path: '/prompts/', method: 'GET', apiFunction: async () => fetch('/api/v2/prompts/') },
    ];
    setEndpoints(allEndpoints);
  }, []);

  const callEndpoint = async (endpoint: any) => {
    setLoading(true);
    setResponse(null);
    
    try {
      let result;
      if (endpoint.apiFunction) {
        // For API functions that use axios
        if (['GET', 'POST', 'PUT', 'DELETE'].includes(endpoint.method)) {
          // Use fetch for direct API calls
          if (endpoint.path.includes('{id}')) {
            result = await endpoint.apiFunction('test-id');
          } else {
            result = await endpoint.apiFunction();
          }
        } else {
          // For specific API functions
          if (endpoint.path.includes('{id}')) {
            result = await endpoint.apiFunction('test-id');
          } else {
            result = await endpoint.apiFunction();
          }
        }
        
        // Handle both fetch response and axios response
        let data;
        let status;
        
        if (result.json) { // It's a fetch response
          status = result.status;
          data = await result.json().catch(() => ({}));
        } else { // It's an axios response
          status = result.status;
          data = result.data;
        }
        
        setResponse({ status, data });
      }
    } catch (error: any) {
      setResponse({ 
        status: error.response?.status || error.status || 'Error', 
        data: error.response?.data || error.message || error 
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">API Explorer</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 bg-white p-4 rounded-lg shadow-md border border-gray-200">
          <h2 className="text-xl font-semibold mb-4">API Endpoints</h2>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {endpoints.map(endpoint => (
              <div 
                key={endpoint.id}
                className={`p-3 rounded cursor-pointer hover:bg-blue-50 ${
                  selectedEndpoint?.id === endpoint.id ? 'bg-blue-100 border border-blue-300' : 'bg-gray-50'
                }`}
                onClick={() => setSelectedEndpoint(endpoint)}
              >
                <div className="font-medium text-sm">{endpoint.name}</div>
                <div className="text-xs text-gray-600 flex justify-between mt-1">
                  <span className="font-mono">{endpoint.path}</span>
                  <span className={`px-2 py-1 rounded ${
                    endpoint.method === 'GET' ? 'bg-green-100 text-green-800' :
                    endpoint.method === 'POST' ? 'bg-blue-100 text-blue-800' :
                    endpoint.method === 'PUT' ? 'bg-yellow-100 text-yellow-800' :
                    endpoint.method === 'DELETE' ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {endpoint.method}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="lg:col-span-2">
          {selectedEndpoint && (
            <div className="bg-white border rounded-lg p-4 shadow-md">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-semibold">{selectedEndpoint.name}</h2>
                <button
                  onClick={() => callEndpoint(selectedEndpoint)}
                  disabled={loading}
                  className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
                >
                  {loading ? 'Loading...' : 'Call Endpoint'}
                </button>
              </div>
              
              <div className="mb-4">
                <div className="font-mono text-sm bg-gray-100 p-2 rounded">
                  {selectedEndpoint.method} /api/v1{selectedEndpoint.path.replace('{id}', 'test-id')}
                </div>
              </div>

              {response && (
                <div className="mt-4">
                  <h3 className="font-semibold mb-2">Response:</h3>
                  <div className={`p-3 rounded ${
                    response.status >= 200 && response.status < 300 
                      ? 'bg-green-50 text-green-800 border border-green-200' 
                      : 'bg-red-50 text-red-800 border border-red-200'
                  }`}>
                    <div className="font-mono text-sm">
                      Status: {response.status}
                    </div>
                    <pre className="mt-2 text-xs overflow-x-auto max-h-60 overflow-y-auto bg-gray-800 text-green-400 p-3 rounded">
                      {JSON.stringify(response.data, null, 2)}
                    </pre>
                  </div>
                </div>
              )}
            </div>
          )}

          {!selectedEndpoint && (
            <div className="bg-white border rounded-lg p-8 text-center">
              <h2 className="text-xl font-semibold mb-2">Select an Endpoint</h2>
              <p className="text-gray-600">Choose an API endpoint from the list to test it</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ApiExplorer;