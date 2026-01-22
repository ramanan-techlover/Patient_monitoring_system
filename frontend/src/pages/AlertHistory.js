import React, { useState } from 'react';
import useMonitoringStore from '../store/monitoringStore';
import '../styles/AlertHistory.css';

function AlertHistory() {
  const { allAlerts } = useMonitoringStore();
  const [filterType, setFilterType] = useState('all');
  const [filterSeverity, setFilterSeverity] = useState('all');

  const filteredAlerts = allAlerts.filter(alert => {
    const typeMatch = filterType === 'all' || alert.type === filterType;
    const severityMatch = filterSeverity === 'all' || alert.severity === filterSeverity;
    return typeMatch && severityMatch;
  });

  const getAlertColor = (severity) => {
    switch (severity) {
      case 'CRITICAL':
        return 'alert-row-critical';
      case 'WARNING':
        return 'alert-row-warning';
      default:
        return 'alert-row-info';
    }
  };

  const stats = {
    total: allAlerts.length,
    critical: allAlerts.filter(a => a.severity === 'CRITICAL').length,
    warning: allAlerts.filter(a => a.severity === 'WARNING').length,
    pain: allAlerts.filter(a => a.type === 'PAIN').length,
    agitation: allAlerts.filter(a => a.type === 'AGITATION').length,
    audio: allAlerts.filter(a => a.type === 'AUDIO').length,
  };

  return (
    <div className="alert-history">
      <div className="history-header">
        <h1>Alert History & Logs</h1>
      </div>

      {/* Statistics */}
      <div className="stats-overview">
        <div className="stat-box">
          <h4>Total Alerts</h4>
          <span className="stat-number">{stats.total}</span>
        </div>
        <div className="stat-box critical">
          <h4>Critical</h4>
          <span className="stat-number">{stats.critical}</span>
        </div>
        <div className="stat-box warning">
          <h4>Warnings</h4>
          <span className="stat-number">{stats.warning}</span>
        </div>
        <div className="stat-box">
          <h4>Pain Alerts</h4>
          <span className="stat-number">{stats.pain}</span>
        </div>
        <div className="stat-box">
          <h4>Agitation</h4>
          <span className="stat-number">{stats.agitation}</span>
        </div>
        <div className="stat-box">
          <h4>Audio</h4>
          <span className="stat-number">{stats.audio}</span>
        </div>
      </div>

      {/* Filters */}
      <div className="filter-section">
        <div className="filter-group">
          <label>Filter by Type:</label>
          <select value={filterType} onChange={(e) => setFilterType(e.target.value)}>
            <option value="all">All Types</option>
            <option value="PAIN">Pain</option>
            <option value="AGITATION">Agitation</option>
            <option value="AUDIO">Audio</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Filter by Severity:</label>
          <select value={filterSeverity} onChange={(e) => setFilterSeverity(e.target.value)}>
            <option value="all">All Severities</option>
            <option value="CRITICAL">Critical</option>
            <option value="WARNING">Warning</option>
          </select>
        </div>
      </div>

      {/* Alerts Table */}
      <div className="table-container">
        <table className="alerts-table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Type</th>
              <th>Severity</th>
              <th>Message</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            {filteredAlerts.length > 0 ? (
              filteredAlerts.map(alert => (
                <tr key={alert.id} className={getAlertColor(alert.severity)}>
                  <td className="time-cell">
                    {new Date(alert.timestamp).toLocaleString()}
                  </td>
                  <td className="type-cell">
                    <span className="badge">{alert.type}</span>
                  </td>
                  <td className="severity-cell">
                    <span className={`severity-badge ${alert.severity.toLowerCase()}`}>
                      {alert.severity}
                    </span>
                  </td>
                  <td className="message-cell">{alert.message}</td>
                  <td className="details-cell">
                    {alert.data && (
                      <details>
                        <summary>View</summary>
                        <pre>{JSON.stringify(alert.data, null, 2)}</pre>
                      </details>
                    )}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5" className="no-data">
                  No alerts found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default AlertHistory;
