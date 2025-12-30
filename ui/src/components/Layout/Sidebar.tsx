import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Sidebar: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <div className="w-64 bg-white shadow-md h-full flex flex-col">
      <div className="p-4 border-b">
        <h2 className="text-xl font-semibold text-gray-800">Suno Prompt Generator</h2>
      </div>
      
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          <li>
            <Link 
              to="/" 
              className={`block px-4 py-2 rounded-md ${
                isActive('/') 
                  ? 'bg-indigo-100 text-indigo-800' 
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              Home
            </Link>
          </li>
          <li>
            <Link 
              to="/prompt-generator" 
              className={`block px-4 py-2 rounded-md ${
                isActive('/prompt-generator') 
                  ? 'bg-indigo-100 text-indigo-800' 
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              Prompt Generator
            </Link>
          </li>
          <li>
            <Link 
              to="/template-library" 
              className={`block px-4 py-2 rounded-md ${
                isActive('/template-library') 
                  ? 'bg-indigo-100 text-indigo-800' 
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              Template Library
            </Link>
          </li>
          <li>
            <Link 
              to="/prompt-history" 
              className={`block px-4 py-2 rounded-md ${
                isActive('/prompt-history') 
                  ? 'bg-indigo-100 text-indigo-800' 
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              Prompt History
            </Link>
          </li>
          <li>
            <Link 
              to="/api-explorer" 
              className={`block px-4 py-2 rounded-md ${
                isActive('/api-explorer') 
                  ? 'bg-indigo-100 text-indigo-800' 
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              API Explorer
            </Link>
          </li>
          <li>
            <Link 
              to="/profile" 
              className={`block px-4 py-2 rounded-md ${
                isActive('/profile') 
                  ? 'bg-indigo-100 text-indigo-800' 
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              Profile
            </Link>
          </li>
        </ul>
      </nav>
      
      <div className="p-4 border-t text-sm text-gray-500">
        <p>Version 1.0.0</p>
      </div>
    </div>
  );
};

export default Sidebar;