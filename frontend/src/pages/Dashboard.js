import React, { useState } from 'react';
import { FiRefreshCw, FiTrendingUp, FiTrendingDown } from 'react-icons/fi';
import useMonitoringStore from '../store/monitoringStore';
import StatCard from '../components/StatCard';
import MonitoringCard from '../components/MonitoringCard';
import AlertCard from '../components/AlertCard';
import '../styles/Dashboard.css';

function Dashboard() {
  const {
    currentPainScore,
    painStatus,
    painHistory,
    currentAgitationLevel,
    agitationStatus,
    agitationHistory,
    detectedKeywords,
    allAlerts,
  } = useMonitoringStore();

  const [refreshing, setRefreshing] = useState(false);

  const handleRefresh = () => {
    setRefreshing(true);
    setTimeout(() => setRefreshing(false), 1000);
  };

  const handleDismissAlert = (alertId) => {
    // In real implementation, would call API to acknowledge alert
    console.log('Alert dismissed:', alertId);
  };

  const criticalAlerts = allAlerts.filter(a => a.severity === 'CRITICAL').slice(0, 5);

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Patient Monitoring Dashboard</h1>
        <button className={`refresh-btn ${refreshing ? 'refreshing' : ''}`} onClick={handleRefresh}>
          <FiRefreshCw /> Refresh
        </button>
      </div>

      {/* Critical Alerts Section */}
      {criticalAlerts.length > 0 && (
        <div className="critical-alerts-section">
          <h2>🚨 Critical Alerts</h2>
          <div className="alerts-grid">
            {criticalAlerts.map(alert => (
              <AlertCard
                key={alert.id}
                alert={alert}
                onDismiss={handleDismissAlert}
              />
            ))}
          </div>
        </div>
      )}

      {/* Key Metrics Section */}
      <div className="metrics-section">
        <h2>Key Metrics</h2>
        <div className="stats-grid">
          <StatCard
            icon={FiTrendingUp}
            title="Pain Score"
            value={(currentPainScore ?? 0).toFixed(2)}
            unit="/5.0"
            status={currentPainScore > 3 ? 'critical' : currentPainScore > 1.5 ? 'warning' : 'normal'}
            trend={`Status: ${painStatus}`}
          />
          <StatCard
            icon={FiTrendingUp}
            title="Agitation Level"
            value={currentAgitationLevel}
            unit="/%"
            status={currentAgitationLevel > 15 ? 'critical' : currentAgitationLevel > 10 ? 'warning' : 'normal'}
            trend={`Status: ${agitationStatus}`}
          />
          <StatCard
            icon={FiTrendingDown}
            title="Total Alerts"
            value={allAlerts.length}
            status="neutral"
            trend={`${criticalAlerts.length} critical`}
          />
          <StatCard
            icon={FiTrendingUp}
            title="Keywords Detected"
            value={detectedKeywords.length}
            status={detectedKeywords.length > 3 ? 'warning' : 'normal'}
            trend={detectedKeywords.join(', ') || 'None'}
          />
        </div>
      </div>

      {/* Monitoring Cards Section */}
      <div className="monitoring-section">
        <h2>Real-time Monitoring</h2>
        <div className="monitoring-grid">
          <MonitoringCard
            title="Pain Detection"
            type="pain"
            currentValue={(currentPainScore ?? 0).toFixed(2)}
            status={painStatus}
            history={painHistory}
            statusColor="#ef4444"
          />
          <MonitoringCard
            title="Agitation Levels"
            type="agitation"
            currentValue={currentAgitationLevel}
            status={agitationStatus}
            history={agitationHistory}
            statusColor="#f59e0b"
          />
        </div>
      </div>

      {/* Recent Alerts */}
      <div className="recent-alerts-section">
        <h2>Recent Activity</h2>
        <div className="alerts-list">
          {allAlerts.length > 0 ? (
            allAlerts.slice(0, 10).map(alert => (
              <div key={alert.id} className="alert-item">
                <span className={`alert-type ${alert.type.toLowerCase()}`}>{alert.type}</span>
                <span className="alert-message-text">{alert.message}</span>
                <span className="alert-time-text">
                  {new Date(alert.timestamp).toLocaleTimeString()}
                </span>
              </div>
            ))
          ) : (
            <p className="no-alerts">No alerts at the moment</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
