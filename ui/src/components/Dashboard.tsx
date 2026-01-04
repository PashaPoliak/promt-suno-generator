import React, { useState, useEffect } from 'react';
import { fetchPlaylists, fetchProfiles, fetchClips } from '../services/api';
import { PlaylistDTO, ProfileDTO, ClipDTO } from '../api/types';

const Dashboard: React.FC = () => {
  const [playlists, setPlaylists] = useState<PlaylistDTO[]>([]);
  const [profiles, setProfiles] = useState<ProfileDTO[]>([]);
  const [clips, setClips] = useState<ClipDTO[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [playlistsData, profilesData, clipsData] = await Promise.all([
          fetchPlaylists(),
          fetchProfiles(),
          fetchClips()
        ]);
        
        setPlaylists(playlistsData);
        setProfiles(profilesData);
        setClips(clipsData);
      } catch (err) {
        setError('Failed to load data. Please try again later.');
        console.error('Error fetching data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <span className="block sm:inline">{error}</span>
      </div>
    );
  }

  return (
    <div className="flex flex-col lg:flex-row gap-8">
      <div className="lg:w-2/3">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-800 mb-4">Popular Playlist</h1>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {playlists.slice(0, 4).map((playlist) => (
              <div key={playlist.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div className="relative">
                  {playlist.image_url ? (
                    <img 
                      src={playlist.image_url} 
                      alt={playlist.name} 
                      className="w-full h-40 object-cover"
                    />
                  ) : (
                    <div className="w-full h-40 bg-gray-200 flex items-center justify-center">
                      <span className="text-gray-500">No Image</span>
                    </div>
                  )}
                
                </div>
                <div className="p-4">
                  <h2 className="font-bold text-lg truncate">{playlist.name}</h2>
                  <p className="text-gray-600 text-sm truncate">{playlist.description || 'No description'}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-800 mb-4">Featured Artists</h1>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {profiles.slice(0, 6).map((profile) => (
              <div key={profile.id} className="flex flex-col items-center">
                <div className="w-16 h-16 rounded-full overflow-hidden border-2 border-indigo-200">
                  {profile.avatar_image_url ? (
                    <img
                      src={profile.avatar_image_url}
                      alt={profile.display_name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full bg-gray-200 flex items-center justify-center">
                      <span className="text-gray-500 text-xs">No Image</span>
                    </div>
                  )}
                </div>
                <p className="mt-2 text-center text-sm truncate w-full">{profile.display_name}</p>
              </div>
            ))}
          </div>
        </div>

        <div>
          <h1 className="text-2xl font-bold text-gray-800 mb-4">Recommended Songs</h1>
          <div className="space-y-2">
            {clips.slice(0, 5).map((clip) => (
              <div key={clip.id} className="flex items-center p-3 bg-white rounded-lg shadow-sm hover:bg-gray-50 transition-colors">
                <div className="w-12 h-12 mr-4">
                  {clip.image_url ? (
                    <img 
                      src={clip.image_url} 
                      alt={clip.title} 
                      className="w-full h-full object-cover rounded"
                    />
                  ) : (
                    <div className="w-full h-full bg-gray-200 flex items-center justify-center">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
                      </svg>
                    </div>
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <h2 className="font-medium truncate">{clip.title}</h2>
                  <p className="text-gray-600 text-sm truncate">{clip.display_name || clip.handle || 'Unknown Artist'}</p>
                </div>
                <span className="text-gray-500 text-sm">
                  {typeof clip.duration === 'number' ?
                    `${Math.floor(clip.duration / 60)}:${(clip.duration % 60).toString().padStart(2, '0')}` :
                    clip.duration || '0:00'}
                </span>
                <button className="ml-4 text-indigo-600 hover:text-indigo-800">
                  Play
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>

    </div>
  );
};

export default Dashboard;
