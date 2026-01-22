import React, { useEffect, useState } from 'react';
import useMonitoringStore from '../store/monitoringStore';
import '../styles/DetailedMonitoring.css';

function AudioMonitoring() {
  const { currentAudioTranscript, detectedKeywords, audioHistory } = useMonitoringStore();
  const [keywordStats, setKeywordStats] = useState({});

  useEffect(() => {
    // Calculate keyword frequency
    const stats = {};
    audioHistory.forEach(item => {
      if (item.keywords) {
        item.keywords.forEach(keyword => {
          stats[keyword] = (stats[keyword] || 0) + 1;
        });
      }
    });
    setKeywordStats(stats);
  }, [audioHistory]);

  return (
    <div className="detailed-monitoring">
      <div className="monitoring-header">
        <h1>Audio Transcription Monitoring</h1>
        <div className="status-indicator">
          <span className={`status-light ${detectedKeywords.length > 0 ? 'orange' : 'green'}`}></span>
          <span>{detectedKeywords.length > 0 ? 'Keywords Detected' : 'Normal'}</span>
        </div>
      </div>

      <div className="monitoring-content">
        <div className="metric-display">
          <div className="metric-box large">
            <h3>Current Transcript</h3>
            <div className="transcript-box">
              {currentAudioTranscript || 'Listening...'}
            </div>
            <p className="metric-description">Last heard audio text</p>
          </div>

          <div className="metric-info-grid">
            <div className="metric-box">
              <h4>Keywords Found</h4>
              <p>{detectedKeywords.length}</p>
            </div>
            <div className="metric-box">
              <h4>Total Transcripts</h4>
              <p>{audioHistory.length}</p>
            </div>
            <div className="metric-box">
              <h4>Last Update</h4>
              <p>
                {audioHistory.length > 0
                  ? new Date(audioHistory[audioHistory.length - 1].timestamp).toLocaleTimeString()
                  : 'N/A'}
              </p>
            </div>
          </div>
        </div>

        <div className="keywords-section">
          <h3>Detected Keywords</h3>
          {detectedKeywords.length > 0 ? (
            <div className="keywords-list">
              {detectedKeywords.map((keyword, idx) => (
                <span key={idx} className="keyword-badge">
                  {keyword}
                  <span className="keyword-count">
                    {keywordStats[keyword] || 0}x
                  </span>
                </span>
              ))}
            </div>
          ) : (
            <p className="no-keywords">No keywords detected</p>
          )}
        </div>

        <div className="analysis-section">
          <h3>Monitored Keywords</h3>
          <div className="keywords-monitored">
            {['help', 'nurse', 'pain', 'doctor', 'emergency', 'breathe', 'hurt', 'ache', 'stop'].map(kw => (
              <div key={kw} className="keyword-item">
                <span className={`keyword-indicator ${detectedKeywords.includes(kw) ? 'detected' : ''}`}>
                  {kw}
                </span>
                <span className="keyword-frequency">
                  {keywordStats[kw] || 0} times
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="transcript-history">
          <h3>Transcript History</h3>
          <div className="history-list">
            {audioHistory.length > 0 ? (
              audioHistory.slice(-20).reverse().map((item, idx) => (
                <div key={idx} className="history-item">
                  <span className="history-time">
                    {new Date(item.timestamp).toLocaleTimeString()}
                  </span>
                  <span className="history-text">{item.text}</span>
                  {item.keywords && item.keywords.length > 0 && (
                    <span className="history-keywords">
                      Keywords: {item.keywords.join(', ')}
                    </span>
                  )}
                </div>
              ))
            ) : (
              <p className="no-history">No transcript history</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default AudioMonitoring;
