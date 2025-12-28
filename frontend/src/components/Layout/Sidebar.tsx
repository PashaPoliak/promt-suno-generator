import React from 'react';

const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-white shadow-md p-4">
      <nav>
        <ul className="space-y-2">
          <li>
            <a 
              href="/" 
              className="block py-2 px-4 rounded hover:bg-indigo-100 transition-colors"
            >
              Dashboard
            </a>
          </li>
          <li>
            <a 
              href="/prompt-generator" 
              className="block py-2 px-4 rounded hover:bg-indigo-100 transition-colors"
            >
              Generate Prompt
            </a>
          </li>
          <li>
            <a 
              href="/template-library" 
              className="block py-2 px-4 rounded hover:bg-indigo-100 transition-colors"
            >
              Template Library
            </a>
          </li>
          <li>
            <a 
              href="/prompt-history" 
              className="block py-2 px-4 rounded hover:bg-indigo-100 transition-colors"
            >
              History
            </a>
          </li>
          <li>
            <a 
              href="/profile" 
              className="block py-2 px-4 rounded hover:bg-indigo-100 transition-colors"
            >
              Profile
            </a>
          </li>
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;