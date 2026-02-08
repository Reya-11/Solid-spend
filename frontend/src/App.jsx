import React, { useState } from 'react';
import DashboardPage from './pages/DashboardPage';
import AnalyticsPage from './pages/AnalyticsPage';

function App() {
  const [view, setView] = useState('dashboard'); // 'dashboard' or 'analytics'

  return (
    <div className="bg-gray-50 min-h-screen">
      <nav className="bg-white shadow-md">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <span className="text-xl font-bold">Expense Tracker</span>
            <div>
              <button
                onClick={() => setView('dashboard')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${view === 'dashboard' ? 'bg-blue-500 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
              >
                Dashboard
              </button>
              <button
                onClick={() => setView('analytics')}
                className={`ml-4 px-3 py-2 rounded-md text-sm font-medium ${view === 'analytics' ? 'bg-blue-500 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
              >
                Analytics
              </button>
            </div>
          </div>
        </div>
      </nav>
      
      <main>
        {view === 'dashboard' && <DashboardPage />}
        {view === 'analytics' && <AnalyticsPage />}
      </main>
    </div>
  );
}

export default App;
