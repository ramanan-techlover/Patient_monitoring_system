import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FiMenu, FiX, FiHome, FiActivity, FiVolume2, FiAlertCircle, FiBarChart2 } from 'react-icons/fi';
import '../styles/Sidebar.css';

function Sidebar() {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const menuItems = [
    { path: '/', label: 'Dashboard', icon: FiHome },
    { path: '/pain', label: 'Pain Monitor', icon: FiActivity },
    { path: '/agitation', label: 'Agitation Monitor', icon: FiBarChart2 },
    { path: '/audio', label: 'Audio Monitor', icon: FiVolume2 },
    { path: '/alerts', label: 'Alert History', icon: FiAlertCircle },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <>
      <button className="sidebar-toggle" onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? <FiX size={24} /> : <FiMenu size={24} />}
      </button>

      <nav className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h1>Pain Watcher</h1>
          <p>Patient Monitoring System</p>
        </div>

        <ul className="sidebar-menu">
          {menuItems.map((item) => {
            const Icon = item.icon;
            return (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`sidebar-link ${isActive(item.path) ? 'active' : ''}`}
                  onClick={() => setIsOpen(false)}
                >
                  <Icon size={20} />
                  <span>{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>

        <div className="sidebar-footer">
          <p>Real-time Monitoring</p>
          <div className="status-indicator online">
            <span></span> Connected
          </div>
        </div>
      </nav>
    </>
  );
}

export default Sidebar;
