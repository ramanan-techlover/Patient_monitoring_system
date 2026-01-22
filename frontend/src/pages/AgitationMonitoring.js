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
import useMonitoringStore from '../store/monitoringStore';
import '../styles/DetailedMonitoring.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
);

function AgitationMonitoring() {
  const { currentAgitationLevel, agitationStatus, agitationHistory } = useMonitoringStore();
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    if (agitationHistory && agitationHistory.length > 0) {
      const labels = agitationHistory.map(item =>
        new Date(item.timestamp).toLocaleTimeString()
      );
      const data = agitationHistory.map(item => item.level);

      setChartData({
        labels,
        datasets: [
          {
            label: 'Agitation Level',
            data,
            borderColor: '#f59e0b',
            backgroundColor: '#f59e0b20',
            borderWidth: 2,
            tension: 0.4,
            fill: true,
            pointRadius: 4,
            pointBackgroundColor: '#f59e0b',
          },
        ],
      });
    }
  }, [agitationHistory]);

  return (
    <div className="detailed-monitoring">
      <div className="monitoring-header">
        <h1>Agitation Detection Monitoring</h1>
        <div className="status-indicator">
          <span className={`status-light ${agitationStatus === 'CALM' ? 'green' : 'red'}`}></span>
          <span>{agitationStatus}</span>
        </div>
      </div>

      <div className="monitoring-content">
        <div className="metric-display">
          <div className="metric-box large">
            <h3>Current Agitation Level</h3>
            <div className="metric-value">{currentAgitationLevel}</div>
            <p className="metric-description">Movement Activity Percentage</p>
          </div>

          <div className="metric-info-grid">
            <div className="metric-box">
              <h4>Status</h4>
              <p>{agitationStatus}</p>
            </div>
            <div className="metric-box">
              <h4>Critical Threshold</h4>
              <p>20</p>
            </div>
            <div className="metric-box">
              <h4>Warning Threshold</h4>
              <p>10</p>
            </div>
            <div className="metric-box">
              <h4>Total Readings</h4>
              <p>{agitationHistory.length}</p>
            </div>
          </div>
        </div>

        {chartData && (
          <div className="chart-container">
            <h3>Agitation Level History</h3>
            <Line
              data={chartData}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: { display: true },
                  tooltip: { mode: 'index', intersect: false },
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    max: 100,
                    title: { display: true, text: 'Level (%)' },
                  },
                },
              }}
              height={300}
            />
          </div>
        )}

        <div className="analysis-section">
          <h3>Movement Detection Analysis</h3>
          <div className="au-grid">
            <div className="au-item">
              <h4>Head Movement</h4>
              <p>Threshold: 0.02 (2% of screen)</p>
              <p>Indicates head tossing or restlessness</p>
            </div>
            <div className="au-item">
              <h4>Arm Movement</h4>
              <p>Threshold: 0.035 (3.5% of screen)</p>
              <p>Weighted 2x more than head movement</p>
            </div>
            <div className="au-item">
              <h4>Agitation Counter</h4>
              <p>Increases on movement, cooldown when still</p>
              <p>Critical alert when > 20</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AgitationMonitoring;
