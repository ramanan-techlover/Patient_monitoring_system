import io from 'socket.io-client';
import { toast } from 'react-toastify';

let socket = null;

const SOCKET_URL = process.env.REACT_APP_SOCKET_URL || 'http://localhost:5000';

export const setupAlertListener = (callback) => {
  if (socket) return;

  socket = io(SOCKET_URL, {
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    reconnectionAttempts: 5,
  });

  socket.on('connect', () => {
    console.log('✓ Connected to monitoring server');
    toast.success('Connected to monitoring system');
  });

  socket.on('pain_alert', (alert) => {
    // Backend already sends complete alert object
    callback(alert);
    if (alert.data && alert.data.score > 3) {
      toast.error(`🚨 PAIN ALERT: ${alert.data.score.toFixed(2)}`);
    }
  });

  socket.on('agitation_alert', (alert) => {
    // Backend already sends complete alert object
    callback(alert);
    if (alert.data && alert.data.level > 15) {
      toast.error(`🚨 AGITATION ALERT: Level ${alert.data.level}`);
    }
  });

  socket.on('audio_alert', (alert) => {
    // Backend already sends complete alert object
    callback(alert);
    if (alert.data && alert.data.keywords && alert.data.keywords.length > 0) {
      toast.warning(`🔊 Keywords: ${alert.data.keywords.join(', ')}`);
    }
  });

  socket.on('disconnect', () => {
    console.log('✗ Disconnected from monitoring server');
    toast.error('Disconnected from monitoring system');
  });

  socket.on('error', (error) => {
    console.error('Socket error:', error);
    toast.error('Connection error');
  });
};

export const closeAlertListener = () => {
  if (socket) {
    socket.disconnect();
    socket = null;
  }
};

export const emitStatusUpdate = (status) => {
  if (socket) {
    socket.emit('status_update', status);
  }
};
