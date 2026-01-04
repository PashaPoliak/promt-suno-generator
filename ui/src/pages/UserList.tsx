import React, { useState, useEffect } from 'react';
import { fetchUsers } from '../services/api';
import { UserDTO } from '../api/types';

const UserList: React.FC = () => {
  const [users, setUsers] = useState<UserDTO[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadUsers = async () => {
      try {
        setLoading(true);
        const data = await fetchUsers();
        setUsers(data);
      } catch (err) {
        setError('Failed to load users');
        console.error('Error loading users:', err);
      } finally {
        setLoading(false);
      }
    };

    loadUsers();
  }, []);

  if (loading) return <div className="text-center py-8">Loading users...</div>;
  if (error) return <div className="text-center py-8 text-red-600">{error}</div>;

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Users</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {users.map(user => (
          <div key={user.id} className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <div className="flex items-center mb-4">
              {user.avatar_image_url ? (
                <img 
                  src={user.avatar_image_url} 
                  alt={user.display_name || user.handle || 'User'} 
                  className="w-16 h-16 rounded-full mr-4"
                />
              ) : (
                <div className="w-16 h-16 rounded-full bg-gray-300 flex items-center justify-center mr-4">
                  <span className="text-gray-600 text-2xl">
                    {user.display_name?.charAt(0) || user.handle?.charAt(0) || '?'}
                  </span>
                </div>
              )}
              <div>
                <h3 className="text-lg font-semibold text-gray-800">
                  {user.display_name || user.handle || 'Unknown User'}
                </h3>
                {user.handle && (
                  <p className="text-gray-600">@{user.handle}</p>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {users.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No users found
        </div>
      )}
    </div>
  );
};

export default UserList;