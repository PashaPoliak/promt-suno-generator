import React, { useState, useRef, useEffect, useCallback } from 'react';
import { ClipDTO, PlaylistClipDTO } from '../api/types';
import { fetchClips } from '../services/api';

interface MusicPlayerProps {
  clips?: (ClipDTO | PlaylistClipDTO)[];
  fetchClipsFromAPI?: boolean;
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

  useEffect(() => {
    if (fetchClipsFromAPI && (!propsClips || propsClips.length === 0)) {
      const fetchClipsFromServer = async () => {
        try {
          setLoadingClips(true);
          setError(null);
          const response = await fetchClips();
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

  const currentClip = clips && clips[currentClipIndex] ? clips[currentClipIndex] : null;

  const formatTime = useCallback((time: number) => {
    if (isNaN(time)) return '0:00';
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  }, []);

  const getClipDuration = useCallback((): string => {
    if (!currentClip) return formatTime(duration);
    
    if ('duration' in currentClip && currentClip.duration !== undefined) {
      if (typeof currentClip.duration === 'number') {
        return formatTime(currentClip.duration);
      } else {
        return currentClip.duration as string;
      }
    }
    
    if ('clip_metadata' in currentClip && currentClip.clip_metadata?.duration) {
      return currentClip.clip_metadata.duration;
    }
    
    return formatTime(duration);
  }, [currentClip, duration, formatTime]);

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
              <span className="text-gray-50 text-xs">No Image</span>
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
      
      const onLoadedMetadata = () => {
        setDuration(audio.duration || 0);
        setIsLoading(false);
      };
      
      audio.addEventListener('loadedmetadata', onLoadedMetadata);
      
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
      <div className="flex flex-col items-center mb-4">
        <div className="w-48 h-48 rounded-lg overflow-hidden shadow-lg mb-4">
          {albumImageUrl ? (
            <img
              src={albumImageUrl}
              alt={`${displayTitle} album cover`}
              className="w-full h-full object-cover"
              onError={(e) => {
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
            <span className="text-gray-500 text-lg">No Album</span>
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
          <span className="text-xl">⏮</span>
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
            <span className="text-xl">⏸</span>
          ) : (
            <span className="text-xl">▶</span>
          )}
        </button>
        
        <button
          onClick={nextTrack}
          disabled={!clips || clips.length <= 1}
          className={`p-2 rounded-full hover:bg-gray-700 ${!clips || clips.length <= 1 ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-70'}`}
          aria-label="Next track"
        >
          <span className="text-xl">⏭</span>
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

      <div className="mt-4 max-h-60 overflow-y-auto bg-gray-800 rounded p-2">
        <h4 className="font-semibold text-gray-30 mb-2">Playlist</h4>
        <div className="space-y-1">
          {playlistItems}
        </div>
      </div>

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