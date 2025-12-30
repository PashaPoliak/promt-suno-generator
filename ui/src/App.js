// App.js
import React, { useState, useEffect, useRef } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { EffectCoverflow } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/effect-coverflow';
import './App.css';

function App() {
  const [songs, setSongs] = useState([]);
  const [currentSongIndex, setCurrentSongIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);
  const audioRef = useRef(null);

  useEffect(() => {
    fetchSongs();
  }, []);

  useEffect(() => {
    if (songs.length > 0) {
      updateSongInfo(currentSongIndex);
    }
  }, [songs, currentSongIndex]);

  const fetchSongs = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/playlist', {
        mode: 'cors',
        headers: {
          'Accept': 'application/json',
        }
      });
      const data = await response.json();
      const formattedSongs = data.map(item => ({
        id: item.id,
        title: item.title,
        name: item.artistName,
        source: item.audioUrl,
        image: item.coverImage
      }));
      setSongs(formattedSongs);
    } catch (error) {
      console.error('Error fetching songs:', error);
    }
  };

  const updateSongInfo = (index) => {
    const song = songs[index];
    if (song && audioRef.current) {
      audioRef.current.src = song.source;
      audioRef.current.load();
      if (isPlaying) {
        audioRef.current.play();
      }
    }
  };

  const playPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const nextSong = () => {
    const nextIndex = (currentSongIndex + 1) % songs.length;
    setCurrentSongIndex(nextIndex);
  };

  const prevSong = () => {
    const prevIndex = (currentSongIndex - 1 + songs.length) % songs.length;
    setCurrentSongIndex(prevIndex);
  };

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setProgress(audioRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration);
    }
  };

  const handleProgressChange = (e) => {
    const value = parseFloat(e.target.value);
    setProgress(value);
    if (audioRef.current) {
      audioRef.current.currentTime = value;
    }
  };

  const handleEnded = () => {
    nextSong();
  };

  const handleSlideChange = (swiper) => {
    setCurrentSongIndex(swiper.activeIndex);
  };

  return (
    <div className="app">
      <div className="album-cover">
        <Swiper
          effect={'coverflow'}
          centeredSlides={true}
          initialSlide={currentSongIndex}
          slidesPerView={'auto'}
          grabCursor={true}
          spaceBetween={40}
          coverflowEffect={{
            rotate: 25,
            stretch: 0,
            depth: 50,
            modifier: 1,
            slideShadows: false,
          }}
          modules={[EffectCoverflow]}
          className="mySwiper"
          onSlideChange={handleSlideChange}
        >
          {songs.map((song, index) => (
            <SwiperSlide key={song.id} className="swiper-slide">
              <img src={song.image} alt={song.title} />
              <div className="overlay">
                <a href={song.source} target="_blank" rel="noopener noreferrer">
                  <ion-icon name="logo-youtube"></ion-icon>
                </a>
              </div>
            </SwiperSlide>
          ))}
        </Swiper>
      </div>

      <div className="music-player">
        <h1>{songs[currentSongIndex]?.title || 'Title'}</h1>
        <p>{songs[currentSongIndex]?.name || 'Song Name'}</p>

        <audio
          ref={audioRef}
          onTimeUpdate={handleTimeUpdate}
          onLoadedMetadata={handleLoadedMetadata}
          onEnded={handleEnded}
          preload="metadata"
        />

        <input
          type="range"
          min="0"
          max={duration}
          value={progress}
          onChange={handleProgressChange}
          className="progress-bar"
        />

        <div className="controls">
          <button className="backward" onClick={prevSong}>
            <i className="fa-solid fa-backward"></i>
          </button>
          <button className="play-pause-btn" onClick={playPause}>
            <i className={`fa-solid ${isPlaying ? 'fa-pause' : 'fa-play'}`}></i>
          </button>
          <button className="forward" onClick={nextSong}>
            <i className="fa-solid fa-forward"></i>
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;