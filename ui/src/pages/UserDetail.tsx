import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { fetchUserById } from '../services/api';
import { UserDTO } from '../api/types';

const UserDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [user, setUser] = useState<UserDTO | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadUser = async () => {
      try {
        setLoading(true);
        const data = await fetchUserById(id!);
        setUser(data);
      } catch (err) {
        setError('Failed to load user');
        console.error('Error loading user:', err);
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      loadUser();
    }
  }, [id]);

  if (loading) return <div className="text-center py-8">Loading user...</div>;
  if (error) return <div className="text-center py-8 text-red-600">{error}</div>;
  if (!user) return <div className="text-center py-8">User not found</div>;

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-20">
        <div className="flex items-center mb-6">
          {user.avatar_image_url ? (
            <img 
              src={user.avatar_image_url} 
              alt={user.display_name || user.handle || 'User'} 
              className="w-24 h-24 rounded-full mr-6"
            />
          ) : (
            <div className="w-24 h-24 rounded-full bg-gray-300 flex items-center justify-center mr-6">
              <span className="text-gray-600 text-3xl">
                {user.display_name?.charAt(0) || user.handle?.charAt(0) || '?'}
              </span>
            </div>
          )}
          <div>
            <h1 className="text-2xl font-bold text-gray-800">
              {user.display_name || user.handle || 'Unknown User'}
            </h1>
            {user.handle && (
              <p className="text-lg text-gray-600">@{user.handle}</p>
            )}
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-gray-50 p-4 rounded border border-gray-200">
            <h2 className="text-lg font-semibold text-gray-800 mb-2">User Information</h2>
            <div className="space-y-2">
              <div>
                <label className="block text-sm font-medium text-gray-700">ID</label>
                <p className="text-gray-900">{user.id}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Display Name</label>
                <p className="text-gray-900">{user.display_name || 'N/A'}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Handle</label>
                <p className="text-gray-900">{user.handle || 'N/A'}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserDetail;