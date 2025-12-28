import React from 'react';

const Profile: React.FC = () => {
  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">User Profile</h1>
      
      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-20">
        <div className="mb-6">
          <h2 className="text-lg font-semibold mb-4">Account Information</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <div className="p-2 bg-gray-50 rounded border border-gray-300">
                user@example.com
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Username
              </label>
              <div className="p-2 bg-gray-50 rounded border border-gray-300">
                username
              </div>
            </div>
          </div>
        </div>
        
        <div>
          <h2 className="text-lg font-semibold mb-4">Preferences</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-70 mb-1">
                Default Prompt Style
              </label>
              <div className="p-2 bg-gray-50 rounded border border-gray-300">
                Custom
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Favorite Genres
              </label>
              <div className="p-2 bg-gray-50 rounded border border-gray-300">
                Pop, Rock, Electronic
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;