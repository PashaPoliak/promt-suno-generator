import React, { useState, useRef, useEffect, useCallback } from 'react';
import { ClipDTO, PlaylistClipDTO } from '../../types';
import { getClips } from '../../../../services/api';

interface MusicPlayerProps {
  clips?: (ClipDTO | PlaylistClipDTO)[];
  fetchClipsFromAPI?: boolean; // If true, fetch clips from API instead of using props
  currentClipIndex?: number;
  onClipChange?: (index: number) => void;
  className?: string;
}

export const MusicPlayer: React.FC<MusicPlayerProps> = ({
  clips: propsClips,
  fetchClipsFromAPI = false,
  currentClipIndex = 0,
  onClipChange,
  className = ''
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(0.7);
  const [isMuted, setIsMuted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [clips, setClips] = useState<(ClipDTO | PlaylistClipDTO)[]>(propsClips || []);
  const [loadingClips, setLoadingClips] = useState(false);
  
  const audioRef = useRef<HTMLAudioElement>(null);
  const progressRef = useRef<HTMLDivElement>(null);

  // Fetch clips from API if needed
  useEffect(() => {
    if (fetchClipsFromAPI && (!propsClips || propsClips.length === 0)) {
      const fetchClipsFromServer = async () => {
        try {
          setLoadingClips(true);
          setError(null);
          const response = await getClips();
          setClips(response);
        } catch (err) {
          setError('Failed to load clips: ' + (err as Error).message);
        } finally {
          setLoadingClips(false);
        }
      };
      
      fetchClipsFromServer();
    } else if (propsClips) {
      setClips(propsClips);
    }
  }, [fetchClipsFromAPI, propsClips]);

  // Get current clip safely
  const currentClip = clips && clips[currentClipIndex] ? clips[currentClipIndex] : null;

  // Format time for display (MM:SS)
  const formatTime = useCallback((time: number) => {
    if (isNaN(time)) return '0:00';
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  }, []);

  // Helper function to get duration from different clip types
  const getClipDuration = useCallback((): string => {
    if (!currentClip) return formatTime(duration);
    
    // Check if it's a ClipDTO with duration
    if ('duration' in currentClip && currentClip.duration !== undefined) {
      if (typeof currentClip.duration === 'number') {
        return formatTime(currentClip.duration);
      } else {
        return currentClip.duration as string;
      }
    }
    
    // Check if it's a PlaylistClipDTO with metadata duration
    if ('clip_metadata' in currentClip && currentClip.clip_metadata?.duration) {
      return currentClip.clip_metadata.duration;
    }
    
    return formatTime(duration);
  }, [currentClip, duration, formatTime]);

  // Toggle play/pause
  const togglePlay = useCallback(() => {
    if (!currentClip?.audio_url) {
      setError('No audio source available for this track');
      return;
    }
    
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
        setIsPlaying(false);
      } else {
        audioRef.current.play().catch(err => {
          setError('Failed to play audio: ' + (err as Error).message);
          setIsPlaying(false);
        }).then(() => {
          if (!error) {
            setIsPlaying(true);
          }
        });
      }
    }
  }, [isPlaying, currentClip, error]);

  // Handle time updates
  const handleTimeUpdate = useCallback(() => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
      setDuration(audioRef.current.duration || 0);
    }
  }, []);

  // Handle seeking in track
  const handleSeek = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    if (!audioRef.current || !progressRef.current || duration <= 0) return;
    
    const progressBar = progressRef.current;
    const clickX = e.clientX - progressBar.getBoundingClientRect().left;
    const width = progressBar.clientWidth;
    if (width <= 0) return; // Avoid division by zero
    
    const percent = Math.max(0, Math.min(1, clickX / width)); // Ensure value is between 0 and 1
    const newTime = percent * duration;
    
    audioRef.current.currentTime = newTime;
    setCurrentTime(newTime);
  }, [duration]);

  // Handle volume changes
  const handleVolumeChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const newVolume = parseFloat(e.target.value);
    setVolume(newVolume);
    setIsMuted(newVolume === 0);
  }, []);

  // Toggle mute
  const toggleMute = useCallback(() => {
    setIsMuted(!isMuted);
  }, [isMuted]);

  // Navigate to next track
  const nextTrack = useCallback(() => {
    if (clips && clips.length > 0) {
      const nextIndex = (currentClipIndex + 1) % clips.length;
      onClipChange?.(nextIndex);
    }
  }, [clips, currentClipIndex, onClipChange]);

  // Navigate to previous track
  const prevTrack = useCallback(() => {
    if (clips && clips.length > 0) {
      const prevIndex = (currentClipIndex - 1 + clips.length) % clips.length;
      onClipChange?.(prevIndex);
    }
  }, [clips, currentClipIndex, onClipChange]);

  // Memoize the playlist rendering for performance
  const playlistItems = React.useMemo(() => {
    if (!clips) return [];
    return clips.map((clip, index) => {
      const albumImage = clip
        ? (clip as ClipDTO).image_url ||
          (clip as ClipDTO).image_large_url ||
          (clip as PlaylistClipDTO).image_url ||
          (clip as PlaylistClipDTO).image_large_url ||
          null
        : null;
      return (
        <div
          key={clip.id}
          onClick={() => onClipChange?.(index)}
          className={`flex items-center p-2 rounded cursor-pointer ${
            index === currentClipIndex
              ? 'bg-indigo-600'
              : 'hover:bg-gray-700'
          }`}
          aria-current={index === currentClipIndex ? 'true' : 'false'}
        >
          <div className="w-8 h-8 rounded mr-2 overflow-hidden flex-shrink-0">
            {albumImage ? (
              <img
                src={albumImage}
                alt={`${clip.title} album cover`}
                className="w-full h-full object-cover"
                onError={(e) => {
                  const imgElement = e.target as HTMLImageElement;
                  imgElement.style.display = 'none';
                  const placeholder = imgElement.parentElement?.querySelector('.playlist-item-placeholder');
                  if (placeholder) {
                    placeholder.setAttribute('style', 'display: flex !important;');
                  }
                }}
              />
            ) : null}
            <div className={`w-full h-full bg-gray-700 flex items-center justify-center ${albumImage ? 'hidden' : 'flex'} playlist-item-placeholder`}>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-gray-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
          <span
            className={`truncate ${
              index === currentClipIndex
                ? 'text-white'
                : 'text-gray-300'
            }`}
          >
            {index + 1}. {clip.title}
          </span>
        </div>
      );
    });
  }, [clips, currentClipIndex, onClipChange]);

  // Handle audio ended event
  const handleAudioEnded = useCallback(() => {
    setIsPlaying(false);
    nextTrack();
  }, [nextTrack]);

  // Handle audio error
  const handleAudioError = useCallback((e: React.SyntheticEvent<HTMLAudioElement, Event>) => {
    setError('Failed to load audio: ' + (e.currentTarget.error?.message || 'Unknown error'));
    setIsPlaying(false);
  }, []);

  // Handle track change effect
  useEffect(() => {
    if (!currentClip) return;

    setIsLoading(true);
    setError(null);
    
    const audio = audioRef.current;
    if (audio) {
      audio.src = currentClip.audio_url || '';
      audio.volume = isMuted ? 0 : volume;
      
      // When metadata is loaded, we can update duration
      const onLoadedMetadata = () => {
        setDuration(audio.duration || 0);
        setIsLoading(false);
      };
      
      audio.addEventListener('loadedmetadata', onLoadedMetadata);
      
      // Play if it was playing before
      if (isPlaying) {
        audio.play().catch(err => {
          setError('Failed to play audio: ' + (err as Error).message);
          setIsPlaying(false);
        });
      }
      
      // Cleanup
      return () => {
        audio.removeEventListener('loadedmetadata', onLoadedMetadata);
      };
    }
  }, [currentClip, isPlaying, volume, isMuted]);

  // Update volume when it changes
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = isMuted ? 0 : volume;
    }
  }, [volume, isMuted]);

  // Reset player when clips change
  useEffect(() => {
    if (clips && clips.length === 0) {
      setIsPlaying(false);
      setCurrentTime(0);
      setDuration(0);
      setError(null);
    }
  }, [clips]);

  // Update volume when it changes
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = isMuted ? 0 : volume;
    }
  }, [volume, isMuted]);

  // Get album image URL from current clip - properly handle both ClipDTO and PlaylistClipDTO types
  const albumImageUrl = currentClip
    ? (currentClip as ClipDTO).image_url ||
      (currentClip as ClipDTO).image_large_url ||
      (currentClip as PlaylistClipDTO).image_url ||
      (currentClip as PlaylistClipDTO).image_large_url ||
      null
    : null;

  const displayTitle = currentClip?.title || 'No track selected';
  const displayDuration = getClipDuration();

  // Reset player when clips change
  useEffect(() => {
    if (clips && clips.length === 0) {
      setIsPlaying(false);
      setCurrentTime(0);
      setDuration(0);
      setError(null);
    }
  }, [clips]);

  if (loadingClips || (fetchClipsFromAPI && (!clips || clips.length === 0))) {
    return (
      <div className={`bg-gray-900 text-white p-6 rounded-lg shadow-lg ${className}`}>
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-gray-400">Loading music...</p>
        </div>
      </div>
    );
  }

  if (!clips || clips.length === 0) {
    return (
      <div className={`bg-gray-900 text-white p-6 rounded-lg shadow-lg ${className}`}>
        <div className="text-center py-8">
          <p className="text-gray-400">No tracks available</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-gray-900 text-white p-4 rounded-lg shadow-lg ${className}`}>
      {error && (
        <div className="mb-4 p-2 bg-red-900 text-red-100 rounded text-sm">
          {error}
        </div>
      )}
      
      {/* Album Art Display */}
      <div className="flex flex-col items-center mb-4">
        <div className="w-48 h-48 rounded-lg overflow-hidden shadow-lg mb-4">
          {albumImageUrl ? (
            <img
              src={albumImageUrl}
              alt={`${displayTitle} album cover`}
              className="w-full h-full object-cover"
              onError={(e) => {
                // If image fails to load, hide the img and show placeholder
                const imgElement = e.target as HTMLImageElement;
                imgElement.style.display = 'none';
                const placeholder = imgElement.parentElement?.querySelector('.album-placeholder');
                if (placeholder) {
                  placeholder.setAttribute('style', 'display: flex !important;');
                }
              }}
            />
          ) : null}
          <div className={`w-full h-full bg-gray-700 flex items-center justify-center ${albumImageUrl ? 'hidden' : 'flex' } album-placeholder`}>
            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
      </div>

      <div className="flex items-center justify-between mb-4">
        <div className="flex-1 min-w-0">
          <h3 className="font-bold text-lg truncate" title={displayTitle}>
            {displayTitle}
          </h3>
          <p className="text-gray-400 text-sm truncate">
            {currentClip?.display_name || currentClip?.handle || 'Unknown Artist'}
          </p>
        </div>
        <div className="text-right ml-4">
          <div className="text-sm text-gray-400">{displayDuration}</div>
        </div>
      </div>

      <div className="flex items-center justify-center space-x-6 mb-4">
        <button
          onClick={prevTrack}
          disabled={!clips || clips.length <= 1}
          className={`p-2 rounded-full hover:bg-gray-700 ${!clips || clips.length <= 1 ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-700'}`}
          aria-label="Previous track"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        
        <button
          onClick={togglePlay}
          disabled={!currentClip?.audio_url}
          className={`p-3 rounded-full ${
            currentClip?.audio_url
              ? 'bg-indigo-600 hover:bg-indigo-700'
              : 'bg-gray-700 cursor-not-allowed'
          }`}
          aria-label={isPlaying ? 'Pause' : 'Play'}
        >
          {isLoading ? (
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
          ) : isPlaying ? (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 0 0118 0z" />
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 00-1.664z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 0 0118 0z" />
            </svg>
          )}
        </button>
        
        <button
          onClick={nextTrack}
          disabled={!clips || clips.length <= 1}
          className={`p-2 rounded-full hover:bg-gray-700 ${!clips || clips.length <= 1 ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-70'}`}
          aria-label="Next track"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <div className="mb-2">
        <div 
          ref={progressRef}
          onClick={handleSeek}
          className="h-2 bg-gray-700 rounded-full cursor-pointer group"
        >
          <div 
            className="h-full bg-indigo-600 rounded-full relative" 
            style={{ width: `${duration ? (currentTime / duration) * 100 : 0}%` }}
          >
            <div className="absolute right-0 -top-1.5 w-4 h-4 bg-white rounded-full opacity-0 group-hover:opacity-100 transform translate-x-1/2 -translate-y-1/2"></div>
          </div>
        </div>
        <div className="flex justify-between text-xs text-gray-400 mt-1">
          <span>{formatTime(currentTime)}</span>
          <span>{formatTime(duration)}</span>
        </div>
      </div>

      <div className="flex items-center space-x-2 mt-3">
        <button 
          onClick={toggleMute} 
          className="p-1 rounded hover:bg-gray-700"
          aria-label={isMuted ? 'Unmute' : 'Mute'}
        >
          {isMuted || volume === 0 ? (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 010 7.072M12 6a9 9 0 010 12m-4.5-9.5L12 3l4.5 4.5M12 2v20" />
            </svg>
          )}
        </button>
        <input
          type="range"
          min="0"
          max="1"
          step="0.01"
          value={volume}
          onChange={handleVolumeChange}
          className="w-full h-1.5 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-indigo-600"
          aria-label="Volume control"
        />
      </div>

      {/* Playlist functionality */}
      <div className="mt-4 max-h-60 overflow-y-auto bg-gray-800 rounded p-2">
        <h4 className="font-semibold text-gray-30 mb-2">Playlist</h4>
        <div className="space-y-1">
          {playlistItems}
        </div>
      </div>

      {/* Hidden audio element */}
      <audio
        ref={audioRef}
        onTimeUpdate={handleTimeUpdate}
        onEnded={handleAudioEnded}
        onError={handleAudioError}
        onCanPlay={() => setIsLoading(false)}
      />
    </div>
  );
};

export default MusicPlayer;