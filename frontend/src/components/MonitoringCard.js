import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js';
import '../styles/MonitoringCard.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
);

function MonitoringCard({ title, type, currentValue, status, history, statusColor }) {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    if (history && history.length > 0) {
      const labels = history.slice(-20).map(item =>
        new Date(item.timestamp).toLocaleTimeString()
      );
      const data = history.slice(-20).map(item => item.value || item.score || item.level);

      setChartData({
        labels,
        datasets: [
          {
            label: title,
            data,
            borderColor: statusColor,
            backgroundColor: `${statusColor}20`,
            tension: 0.4,
            fill: true,
          },
        ],
      });
    }
  }, [history, title, statusColor]);

  const getStatusBadge = () => {
    const colorMap = {
      'COMFORT': 'badge-green',
      'CALM': 'badge-green',
      'PAIN DETECTED': 'badge-red',
      'Warning: Restless': 'badge-yellow',
      'CRITICAL: PATIENT THRASHING': 'badge-red',
    };
    return colorMap[status] || 'badge-gray';
  };

  return (
    <div className="monitoring-card">
      <div className="card-header">
        <h3>{title}</h3>
        <span className={`status-badge ${getStatusBadge()}`}>{status}</span>
      </div>

      <div className="card-current-value">
        <span className="current-label">Current Value</span>
        <span className="current-value">{currentValue}</span>
      </div>

      {chartData && (
        <div className="card-chart">
          <Line
            data={chartData}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: { display: false },
                tooltip: { mode: 'index', intersect: false },
              },
              scales: {
                y: { beginAtZero: true },
              },
            }}
            height={150}
          />
        </div>
      )}

      <div className="card-stats">
        <div className="stat">
          <span className="stat-label">Readings</span>
          <span className="stat-value">{history?.length || 0}</span>
        </div>
        <div className="stat">
          <span className="stat-label">Last Update</span>
          <span className="stat-value">
            {history?.[history.length - 1]
              ? new Date(history[history.length - 1].timestamp).toLocaleTimeString()
              : 'N/A'}
          </span>
        </div>
      </div>
    </div>
  );
}

export default MonitoringCard;
