import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { MusicPlayer } from './components/MusicPlayer';
import Home from './pages/Home';
import Profile from './pages/Profile';
import Header from './components/Header';

function App() {
 return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Header />
        <div className="flex">
          <main className="flex-1 p-8">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/clips" element={<MusicPlayer fetchClipsFromAPI={true} />} />
              <Route path="/clips/:id" element={<MusicPlayer fetchClipsFromAPI={true} />} />
              <Route path="/playlists" element={<MusicPlayer fetchClipsFromAPI={true} />} />
              <Route path="/playlists/:id" element={<MusicPlayer fetchClipsFromAPI={true} />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
