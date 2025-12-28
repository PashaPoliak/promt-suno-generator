import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Header from './components/Layout/Header';
import Sidebar from './components/Layout/Sidebar';
import Home from './pages/Home';
import PromptGenerator from './pages/PromptGenerator';
import TemplateLibrary from './pages/TemplateLibrary';
import PromptHistory from './pages/PromptHistory';
import Profile from './pages/Profile';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="flex flex-col min-h-screen">
          <Header />
          <div className="flex flex-1">
            <Sidebar />
            <main className="flex-1 p-6 bg-gray-50">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/prompt-generator" element={<PromptGenerator />} />
                <Route path="/template-library" element={<TemplateLibrary />} />
                <Route path="/prompt-history" element={<PromptHistory />} />
                <Route path="/profile" element={<Profile />} />
              </Routes>
            </main>
          </div>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;