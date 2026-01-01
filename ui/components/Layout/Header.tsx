import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="bg-indigo-600 text-white p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-xl font-bold">Suno Prompt Generator</h1>
        <nav>
          <ul className="flex space-x-4">
            <li>
              <a href="/" className="hover:text-indigo-200 transition-colors">
                Home
              </a>
            </li>
            <li>
              <a href="/prompt-generator" className="hover:text-indigo-200 transition-colors">
                Prompt Generator
              </a>
            </li>
            <li>
              <a href="/template-library" className="hover:text-indigo-200 transition-colors">
                Templates
              </a>
            </li>
            <li>
              <a href="/profile" className="hover:text-indigo-200 transition-colors">
                Profile
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </header>
 );
};

export default Header;