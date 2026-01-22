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

function PainMonitoring() {
  const { currentPainScore, painStatus, painHistory } = useMonitoringStore();
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    if (painHistory && painHistory.length > 0) {
      const labels = painHistory.map(item =>
        new Date(item.timestamp).toLocaleTimeString()
      );
      const data = painHistory.map(item => item.score);

      setChartData({
        labels,
        datasets: [
          {
            label: 'Pain Score',
            data,
            borderColor: '#ef4444',
            backgroundColor: '#ef444420',
            borderWidth: 2,
            tension: 0.4,
            fill: true,
            pointRadius: 4,
            pointBackgroundColor: '#ef4444',
          },
        ],
      });
    }
  }, [painHistory]);

  return (
    <div className="detailed-monitoring">
      <div className="monitoring-header">
        <h1>Pain Detection Monitoring</h1>
        <div className="status-indicator">
          <span className={`status-light ${painStatus === 'COMFORT' ? 'green' : 'red'}`}></span>
          <span>{painStatus}</span>
        </div>
      </div>

      <div className="monitoring-content">
        <div className="metric-display">
          <div className="metric-box large">
            <h3>Current Pain Score</h3>
            <div className="metric-value">{(currentPainScore ?? 0).toFixed(2)}</div>
            <p className="metric-description">Grimace Muscle Activity (AU04, AU07, AU10)</p>
          </div>

          <div className="metric-info-grid">
            <div className="metric-box">
              <h4>Status</h4>
              <p>{painStatus}</p>
            </div>
            <div className="metric-box">
              <h4>Threshold</h4>
              <p>1.5</p>
            </div>
            <div className="metric-box">
              <h4>Total Readings</h4>
              <p>{painHistory.length}</p>
            </div>
            <div className="metric-box">
              <h4>Last Update</h4>
              <p>
                {painHistory.length > 0
                  ? new Date(painHistory[painHistory.length - 1].timestamp).toLocaleTimeString()
                  : 'N/A'}
              </p>
            </div>
          </div>
        </div>

        {chartData && (
          <div className="chart-container">
            <h3>Pain Score History</h3>
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
                    max: 5,
                    title: { display: true, text: 'Score' },
                  },
                },
              }}
              height={300}
            />
          </div>
        )}

        <div className="analysis-section">
          <h3>Action Units Analysis</h3>
          <div className="au-grid">
            <div className="au-item">
              <h4>AU04 - Brow Lowerer</h4>
              <p>Indicates pain and concentration</p>
            </div>
            <div className="au-item">
              <h4>AU07 - Lid Tightener</h4>
              <p>Eye squinting from pain or emotion</p>
            </div>
            <div className="au-item">
              <h4>AU10 - Upper Lip Raiser</h4>
              <p>Grimace or pain expression</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PainMonitoring;
