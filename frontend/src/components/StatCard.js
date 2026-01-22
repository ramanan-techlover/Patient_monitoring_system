import React from 'react';
import '../styles/StatCard.css';

function StatCard({ icon: Icon, title, value, unit, status, trend }) {
  const getStatusColor = (status) => {
    switch (status) {
      case 'critical':
        return 'stat-critical';
      case 'warning':
        return 'stat-warning';
      case 'normal':
        return 'stat-normal';
      default:
        return 'stat-neutral';
    }
  };

  return (
    <div className={`stat-card ${getStatusColor(status)}`}>
      <div className="stat-icon">
        <Icon size={32} />
      </div>
      <div className="stat-content">
        <h4>{title}</h4>
        <div className="stat-value-container">
          <span className="stat-value">{value}</span>
          {unit && <span className="stat-unit">{unit}</span>}
        </div>
        {trend && <p className="stat-trend">{trend}</p>}
      </div>
      <div className="stat-indicator"></div>
    </div>
  );
}

export default StatCard;
