import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './styles/App.css';

import Dashboard from './pages/Dashboard';
import PainMonitoring from './pages/PainMonitoring';
import AgitationMonitoring from './pages/AgitationMonitoring';
import AudioMonitoring from './pages/AudioMonitoring';
import AlertHistory from './pages/AlertHistory';
import Sidebar from './components/Sidebar';
import useMonitoringStore from './store/monitoringStore';

function App() {
  const initializeAlertSystem = useMonitoringStore(state => state.initializeAlertSystem);

  useEffect(() => {
    // Initialize real-time monitoring
    initializeAlertSystem();
  }, [initializeAlertSystem]);

  return (
    <Router>
      <div className="app-container">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/pain" element={<PainMonitoring />} />
            <Route path="/agitation" element={<AgitationMonitoring />} />
            <Route path="/audio" element={<AudioMonitoring />} />
            <Route path="/alerts" element={<AlertHistory />} />
          </Routes>
        </main>
        <ToastContainer
          position="top-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={true}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />
      </div>
    </Router>
  );
}

export default App;
