import React, { useState, useEffect } from 'react';
import { fetchProfiles } from '../services/api';
import { ProfileDTO } from '../api/types';

const Profile: React.FC = () => {
  const [profiles, setProfiles] = useState<ProfileDTO[]>([]);
  const [loading, setLoading] = useState(true);
 const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadProfiles = async () => {
      try {
        setLoading(true);
        const data = await fetchProfiles();
        setProfiles(data);
      } catch (err) {
        setError('Failed to load profiles');
        console.error('Error loading profiles:', err);
      } finally {
        setLoading(false);
      }
    };

    loadProfiles();
  }, []);

  if (loading) return <div className="text-center py-8">Loading profiles...</div>;
  if (error) return <div className="text-center py-8 text-red-600">{error}</div>;

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Profiles</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {profiles.map(profile => (
          <div key={profile.id} className="bg-white p-6 rounded-lg shadow-md border-gray-200">
            <div className="flex items-center mb-4">
              {profile.avatar_image_url ? (
                <img
                  src={profile.avatar_image_url}
                  alt={profile.display_name || profile.handle || 'Profile'}
                  className="w-16 h-16 rounded-full mr-4"
                />
              ) : (
                <div className="w-16 h-16 rounded-full bg-gray-300 flex items-center justify-center mr-4">
                  <span className="text-gray-600 text-2xl">
                    {profile.display_name?.charAt(0) || profile.handle?.charAt(0) || '?'}
                  </span>
                </div>
              )}
              <div>
                <h3 className="text-lg font-semibold text-gray-800">
                  {profile.display_name || profile.handle || 'Unknown Profile'}
                </h3>
                {profile.handle && (
                  <p className="text-gray-600">@{profile.handle}</p>
                )}
              </div>
            </div>
          
            {profile.profile_description && (
              <div className="mt-4">
                <p className="text-gray-700">{profile.profile_description}</p>
              </div>
            )}
            
            {profile.clips && profile.clips.length > 0 && (
              <div className="mt-4">
                <h4 className="font-medium text-gray-800">Clips ({profile.clips.length})</h4>
                <ul className="mt-2 space-y-1">
                  {profile.clips.slice(0, 3).map(clip => (
                    <li key={clip.id} className="text-sm text-gray-600 truncate">
                      {clip.title}
                    </li>
                  ))}
                  {profile.clips.length > 3 && (
                    <li className="text-sm text-gray-500">+{profile.clips.length - 3} more</li>
                  )}
                </ul>
              </div>
            )}
            
            {profile.playlists && profile.playlists.length > 0 && (
              <div className="mt-4">
                <h4 className="font-medium text-gray-800">Playlists ({profile.playlists.length})</h4>
                <ul className="mt-2 space-y-1">
                  {profile.playlists.slice(0, 3).map(playlist => (
                    <li key={playlist.id} className="text-sm text-gray-600 truncate">
                      {playlist.name}
                    </li>
                  ))}
                  {profile.playlists.length > 3 && (
                    <li className="text-sm text-gray-500">+{profile.playlists.length - 3} more</li>
                  )}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
      
      {profiles.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No profiles found
        </div>
      )}
    </div>
  );
};

export default Profile;