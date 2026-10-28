/**
 * ========================================================================================
 * AirIQ: Multi-City Airbnb Price Intelligence & Predictive Analytics Platform
 * COMPONENT: Layout.jsx — Application Master Shell & Navigation Router
 * ========================================================================================
 * Authors:       Aditya Raju Pidurkar (Roll No. 40), Nidhi Singh (Roll No. 15)
 * Course:        Big Data Analytics (BDA) Laboratory Project
 * Institution:   Department of CSE, Ramdeobaba University (RBU), Nagpur
 * Faculty Guide: Dr. Preeti G. Khante
 *
 * KEY RESPONSIBILITIES:
 * 1. Global Navigation Architecture: Provides persistent sidebar links across Overview Dashboard,
 *    Price Prediction, Geographic Explorer, and Model Evaluation.
 * 2. Visual Identity & Branding: Houses the official Airbnb Coral (#FF5A5F) emblem and
 *    academic institutional attribution headers.
 * 3. Cluster Telemetry Sidebar: Summarizes the active technology stack (PySpark 4.2, Cassandra 4.1,
 *    FastAPI 1.2, React 19) directly within the user layout.
 * ========================================================================================
 */

import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, TrendingUp, MapPin, Award, Activity } from 'lucide-react';

export default function Layout({ children }) {
  // Navigation links corresponding to application route paths
  const navItems = [
    { to: '/', label: 'Overview Dashboard', icon: LayoutDashboard },
    { to: '/predict', label: 'Price Prediction', icon: TrendingUp },
    { to: '/explorer', label: 'Geographic Explorer', icon: MapPin },
    { to: '/evaluation', label: 'Model Evaluation', icon: Award },
  ];

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 flex flex-col font-sans">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-rose-50 border border-rose-200 flex items-center justify-center p-1.5 shadow-xs">
              <svg viewBox="0 0 32 32" fill="#FF5A5F" className="w-5 h-5">
                <path d="M16 1c2.008 0 3.463.963 4.751 3.269l.533 1.025c1.954 3.83 6.18 12.515 6.18 16.206 0 5.8-4.437 10.5-11.464 10.5S4.536 27.3 4.536 21.5c0-3.691 4.226-12.376 6.18-16.206l.533-1.025C12.537 1.963 13.992 1 16 1zm0 2c-1.353 0-2.316.63-3.327 2.433l-.533 1.025C10.219 10.22 6.536 18.069 6.536 21.5c0 4.694 3.486 8.5 9.464 8.5s9.464-3.806 9.464-8.5c0-3.431-3.683-11.28-5.604-15.042l-.533-1.025C18.316 3.63 17.353 3 16 3zm0 13c3.038 0 5.5 2.462 5.5 5.5 0 2.82-1.953 5.105-4.502 5.448L16 27c-3.038 0-5.5-2.462-5.5-5.5 0-2.82 1.953-5.105 4.502-5.448L16 16zm0 2c-1.933 0-3.5 1.567-3.5 3.5 0 1.77 1.258 3.238 2.923 3.465L16 25c1.933 0 3.5-1.567 3.5-3.5 0-1.77-1.258-3.238-2.923-3.465L16 18z"/>
              </svg>
            </div>
            <div>
              <h1 className="text-base font-semibold text-slate-900 leading-tight">AirIQ</h1>
              <p className="text-xs text-slate-500">Airbnb Price Intelligence • Distributed Spark & Cassandra</p>
            </div>
          </div>

          <div></div>
        </div>
      </header>

      {/* Main Container */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 w-full flex-1 flex flex-col md:flex-row gap-6">
        {/* Navigation Sidebar */}
        <aside className="w-full md:w-64 shrink-0">
          <nav className="bg-white border border-slate-200 rounded-lg p-2 space-y-1 shadow-xs">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    `flex items-center space-x-3 px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-slate-900 text-white shadow-xs'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                    }`
                  }
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>

          {/* Quick System Info Box */}
          <div className="mt-4 bg-white border border-slate-200 rounded-lg p-4 text-xs text-slate-500 space-y-2">
            <div className="font-semibold text-slate-700 flex items-center space-x-1.5">
              <Activity className="w-3.5 h-3.5 text-slate-500" />
              <span>Stack Status</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-100">
              <span>Backend API</span>
              <span className="text-slate-700 font-mono">127.0.0.1:8001</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-100">
              <span>Spark MLlib</span>
              <span className="text-slate-700 font-mono">PySpark 4.2</span>
            </div>
            <div className="flex justify-between py-1">
              <span>Cassandra NoSQL</span>
              <span className="text-slate-700 font-mono">Port 9042</span>
            </div>
          </div>
        </aside>

        {/* Content Area */}
        <main className="flex-1 bg-white border border-slate-200 rounded-lg p-6 shadow-xs">
          {children}
        </main>
      </div>

      <footer className="border-t border-slate-200 bg-white py-4 text-center text-xs text-slate-500">
        AirIQ: Airbnb Price Intelligence Platform — Academic Big Data Analytics (BDA) Setup
      </footer>
    </div>
  );
}
