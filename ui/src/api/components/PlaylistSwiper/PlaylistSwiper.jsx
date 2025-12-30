import React, { useState, useEffect } from 'react';
import { getPlaylist } from '../../../../services/api';

const PlaylistSwiper = ({ playlistId, playlistName }) => {
  const [songs, setSongs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPlaylistSongs = async () => {
      try {
        setLoading(true);
        // Fetch actual playlist data from the API
        const playlistData = await getPlaylist(playlistId);
        // Extract songs/clips from the playlist data
        // The structure depends on the API response - this is a common pattern
        const playlistSongs = playlistData.clips || playlistData.songs || playlistData.items || [];
        setSongs(playlistSongs);
      } catch (err) {
        setError('Failed to load playlist songs');
        console.error('Error fetching playlist songs:', err);
        // Fallback to empty array if there's an error
        setSongs([]);
      } finally {
        setLoading(false);
      }
    };

    if (playlistId) {
      fetchPlaylistSongs();
    }
  }, [playlistId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-32">
        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500 text-sm py-2">
        Error: {error}
      </div>
    );
  }

  if (!songs || songs.length === 0) {
    return (
      <div className="text-gray-500 text-sm py-2">
        No songs in this playlist
      </div>
    );
  }

  return (
    <div className="mt-3">
      <div className="relative overflow-hidden">
        <div className="flex space-x-2 overflow-x-auto pb-2" style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}>
          {songs.map((song) => (
            <div key={song.id || song._id} className="flex-shrink-0 w-32">
              <div className="relative group">
                <img
                  src={song.thumbnail || song.imageUrl || 'https://via.placeholder.com/150'}
                  alt={song.title || song.name}
                  className="w-full h-24 object-cover rounded-md"
                />
                <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity rounded-md">
                  <button className="text-white text-xl">
                    ▶
                  </button>
                </div>
              </div>
              <div className="mt-1">
                <div className="text-xs font-medium truncate">{song.title || song.name || 'Unknown Title'}</div>
                <div className="text-xs text-gray-500 truncate">{song.artist || song.author || 'Unknown Artist'}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PlaylistSwiper;