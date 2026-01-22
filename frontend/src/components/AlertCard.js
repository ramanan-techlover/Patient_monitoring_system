import React from 'react';
import { FiAlertTriangle, FiX } from 'react-icons/fi';
import '../styles/AlertCard.css';

function AlertCard({ alert, onDismiss }) {
  const getSeverityClass = (severity) => {
    switch (severity) {
      case 'CRITICAL':
        return 'alert-critical';
      case 'WARNING':
        return 'alert-warning';
      default:
        return 'alert-info';
    }
  };

  return (
    <div className={`alert-card ${getSeverityClass(alert.severity)}`}>
      <div className="alert-header">
        <div className="alert-icon-title">
          <FiAlertTriangle size={20} />
          <div>
            <h4>{alert.type}</h4>
            <p className="alert-time">
              {new Date(alert.timestamp).toLocaleTimeString()}
            </p>
          </div>
        </div>
        <button className="alert-dismiss" onClick={() => onDismiss(alert.id)}>
          <FiX size={20} />
        </button>
      </div>
      <p className="alert-message">{alert.message}</p>
      <div className="alert-details">
        <span className={`severity-badge ${alert.severity.toLowerCase()}`}>
          {alert.severity}
        </span>
      </div>
    </div>
  );
}

export default AlertCard;
