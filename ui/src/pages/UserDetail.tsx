import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getUser } from '../services/api';

interface Clip {
  id: string;
  title: string;
  description?: string;
  audio_url?: string;
  image_url?: string;
}

interface Playlist {
  id: string;
  name: string;
  description?: string;
  clips: Clip[];
}

interface User {
  id: string;
  handle?: string;
  display_name?: string;
  profile_description?: string;
  avatar_image_url?: string;
  clips: Clip[];
  playlists: Playlist[];
}

const UserDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const userData = await getUser(id!);
        setUser(userData);
      } catch (err) {
        setError('Failed to fetch user');
        console.error('Error fetching user:', err);
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchUser();
    }
  }, [id]);

 if (loading) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">User Profile</h1>
        <p className="text-gray-600">Loading user...</p>
      </div>
    );
  }

  if (error || !user) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <h1 className="text-2xl font-bold text-gray-80 mb-6">User Profile</h1>
        <p className="text-red-600">Error: {error || 'User not found'}</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <Link 
          to="/users" 
          className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
        >
          ← Back to Users
        </Link>
      </div>
      
      <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 mb-6">
        <div className="flex items-center space-x-6">
          <img 
            src={user.avatar_image_url || 'https://via.placeholder.com/128'} 
            alt={user.display_name || user.handle || 'User'} 
            className="w-32 h-32 rounded-full object-cover border-4 border-gray-200"
          />
          <div>
            <h1 className="text-2xl font-bold text-gray-800">{user.display_name || user.handle || 'Unknown User'}</h1>
            <p className="text-gray-600 text-lg">{user.handle ? `@${user.handle}` : ''}</p>
            <p className="text-gray-700 mt-2">{user.profile_description}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* User Clips */}
        <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Clips</h2>
          {user.clips && user.clips.length > 0 ? (
            <div className="space-y-4">
              {user.clips.map((clip) => (
                <div key={clip.id} className="flex items-center space-x-4 p-3 border border-gray-200 rounded-lg">
                  <img 
                    src={clip.image_url || 'https://via.placeholder.com/64x64'} 
                    alt={clip.title} 
                    className="w-16 h-16 rounded object-cover"
                  />
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-800">{clip.title}</h3>
                    <p className="text-sm text-gray-600 truncate">{clip.description}</p>
                  </div>
                  {clip.audio_url && (
                    <audio controls className="w-32">
                      <source src={clip.audio_url} type="audio/mpeg" />
                      Your browser does not support the audio element.
                    </audio>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-600">No clips available</p>
          )}
        </div>

        {/* User Playlists */}
        <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Playlists</h2>
          {user.playlists && user.playlists.length > 0 ? (
            <div className="space-y-4">
              {user.playlists.map((playlist) => (
                <div key={playlist.id} className="border border-gray-200 rounded-lg p-4">
                  <h3 className="font-medium text-gray-800 text-lg">{playlist.name}</h3>
                  <p className="text-sm text-gray-600 mb-2">{playlist.description}</p>
                  <div className="mt-2">
                    <p className="text-xs text-gray-50 mb-2">Clips ({playlist.clips.length}):</p>
                    <div className="space-y-2 max-h-60 overflow-y-auto">
                      {playlist.clips.map((clip) => (
                        <div key={clip.id} className="flex items-center space-x-2 text-sm">
                          <span className="text-gray-700 truncate">{clip.title}</span>
                          {clip.audio_url && (
                            <audio controls className="w-24">
                              <source src={clip.audio_url} type="audio/mpeg" />
                              Your browser does not support the audio element.
                            </audio>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-600">No playlists available</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserDetail;