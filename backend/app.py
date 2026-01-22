"""
Backend API Server for Pain Watcher
Integrates with Python monitoring scripts via REST API and WebSocket
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from datetime import datetime, timedelta
from collections import deque
import threading
import queue
import json
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# ============================================================================
# DATA STORAGE (In-Memory)
# ============================================================================

# Store recent data for quick retrieval
class MonitoringData:
    def __init__(self, max_size=200):
        self.pain_history = deque(maxlen=max_size)
        self.agitation_history = deque(maxlen=max_size)
        self.audio_history = deque(maxlen=max_size)
        self.alerts = deque(maxlen=100)
        
        self.current_pain = {'score': 0, 'status': 'COMFORT', 'timestamp': None}
        self.current_agitation = {'level': 0, 'status': 'CALM', 'timestamp': None}
        self.current_audio = {'text': '', 'keywords': [], 'timestamp': None}
        
        self.lock = threading.Lock()

data_store = MonitoringData()

# ============================================================================
# ALERT ROUTES
# ============================================================================

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get all alerts with optional limit"""
    limit = request.args.get('limit', default=50, type=int)
    alerts = list(data_store.alerts)[-limit:]
    return jsonify({'alerts': alerts, 'total': len(data_store.alerts)})

@app.route('/api/alerts/critical', methods=['GET'])
def get_critical_alerts():
    """Get only critical alerts"""
    critical = [a for a in data_store.alerts if a.get('severity') == 'CRITICAL']
    return jsonify({'alerts': critical, 'total': len(critical)})

@app.route('/api/alerts/<alert_id>/acknowledge', methods=['POST'])
def acknowledge_alert(alert_id):
    """Mark an alert as acknowledged"""
    return jsonify({'status': 'acknowledged', 'alert_id': alert_id})

# ============================================================================
# PAIN MONITORING ROUTES
# ============================================================================

@app.route('/api/pain/status', methods=['GET'])
def get_pain_status():
    """Get current pain detection status"""
    with data_store.lock:
        return jsonify(data_store.current_pain)

@app.route('/api/pain/history', methods=['GET'])
def get_pain_history():
    """Get pain detection history"""
    limit = request.args.get('limit', default=100, type=int)
    with data_store.lock:
        history = list(data_store.pain_history)[-limit:]
    return jsonify({'history': history, 'total': len(data_store.pain_history)})

@app.route('/api/pain/update', methods=['POST'])
def update_pain_status():
    """Update pain detection data (called by monitoring script)"""
    data = request.get_json()
    
    with data_store.lock:
        pain_entry = {
            'score': data.get('score', 0),
            'status': data.get('status', 'COMFORT'),
            'au04': data.get('au04'),
            'au07': data.get('au07'),
            'au10': data.get('au10'),
            'timestamp': datetime.now().isoformat(),
        }
        
        data_store.pain_history.append(pain_entry)
        data_store.current_pain = pain_entry
        
        # Create alert if pain detected
        if pain_entry['status'] == 'PAIN DETECTED' and pain_entry['score'] > 1.5:
            alert = {
                'id': f"pain_{datetime.now().timestamp()}",
                'type': 'PAIN',
                'severity': 'CRITICAL' if pain_entry['score'] > 3 else 'WARNING',
                'timestamp': datetime.now().isoformat(),
                'message': f"Pain Detected: Score {pain_entry['score']:.2f}",
                'data': pain_entry,
            }
            data_store.alerts.append(alert)
            socketio.emit('pain_alert', alert)
    
    return jsonify({'status': 'updated', 'data': pain_entry})

# ============================================================================
# AGITATION MONITORING ROUTES
# ============================================================================

@app.route('/api/agitation/status', methods=['GET'])
def get_agitation_status():
    """Get current agitation detection status"""
    with data_store.lock:
        return jsonify(data_store.current_agitation)

@app.route('/api/agitation/history', methods=['GET'])
def get_agitation_history():
    """Get agitation detection history"""
    limit = request.args.get('limit', default=100, type=int)
    with data_store.lock:
        history = list(data_store.agitation_history)[-limit:]
    return jsonify({'history': history, 'total': len(data_store.agitation_history)})

@app.route('/api/agitation/update', methods=['POST'])
def update_agitation_status():
    """Update agitation detection data (called by monitoring script)"""
    data = request.get_json()
    
    with data_store.lock:
        agitation_entry = {
            'level': data.get('level', 0),
            'status': data.get('status', 'CALM'),
            'head_speed': data.get('head_speed'),
            'arm_speed': data.get('arm_speed'),
            'timestamp': datetime.now().isoformat(),
        }
        
        data_store.agitation_history.append(agitation_entry)
        data_store.current_agitation = agitation_entry
        
        # Create alert if agitated
        if agitation_entry['level'] > 10:
            alert = {
                'id': f"agitation_{datetime.now().timestamp()}",
                'type': 'AGITATION',
                'severity': 'CRITICAL' if agitation_entry['level'] > 20 else 'WARNING',
                'timestamp': datetime.now().isoformat(),
                'message': f"Agitation Level: {agitation_entry['level']}",
                'data': agitation_entry,
            }
            data_store.alerts.append(alert)
            socketio.emit('agitation_alert', alert)
    
    return jsonify({'status': 'updated', 'data': agitation_entry})

# ============================================================================
# AUDIO MONITORING ROUTES
# ============================================================================

@app.route('/api/audio/status', methods=['GET'])
def get_audio_status():
    """Get current audio transcription status"""
    with data_store.lock:
        return jsonify(data_store.current_audio)

@app.route('/api/audio/history', methods=['GET'])
def get_audio_history():
    """Get audio transcription history"""
    limit = request.args.get('limit', default=100, type=int)
    with data_store.lock:
        history = list(data_store.audio_history)[-limit:]
    return jsonify({'history': history, 'total': len(data_store.audio_history)})

@app.route('/api/audio/update', methods=['POST'])
def update_audio_status():
    """Update audio transcription data (called by monitoring script)"""
    data = request.get_json()
    
    with data_store.lock:
        audio_entry = {
            'text': data.get('text', ''),
            'keywords': data.get('keywords', []),
            'confidence': data.get('confidence'),
            'timestamp': datetime.now().isoformat(),
        }
        
        data_store.audio_history.append(audio_entry)
        data_store.current_audio = audio_entry
        
        # Create alert if keywords detected
        if audio_entry['keywords']:
            alert = {
                'id': f"audio_{datetime.now().timestamp()}",
                'type': 'AUDIO',
                'severity': 'WARNING',
                'timestamp': datetime.now().isoformat(),
                'message': f"Keywords Detected: {', '.join(audio_entry['keywords'])}",
                'data': audio_entry,
            }
            data_store.alerts.append(alert)
            socketio.emit('audio_alert', alert)
    
    return jsonify({'status': 'updated', 'data': audio_entry})

# ============================================================================
# SYSTEM STATUS ROUTES
# ============================================================================

@app.route('/api/system/status', methods=['GET'])
def get_system_status():
    """Get overall system status"""
    with data_store.lock:
        return jsonify({
            'pain': data_store.current_pain,
            'agitation': data_store.current_agitation,
            'audio': data_store.current_audio,
            'stats': {
                'total_pain_readings': len(data_store.pain_history),
                'total_agitation_readings': len(data_store.agitation_history),
                'total_audio_readings': len(data_store.audio_history),
                'total_alerts': len(data_store.alerts),
                'critical_alerts': len([a for a in data_store.alerts if a.get('severity') == 'CRITICAL']),
            }
        })

# ============================================================================
# CONTROL ROUTES
# ============================================================================

@app.route('/api/monitoring/<monitor_type>/start', methods=['POST'])
def start_monitoring(monitor_type):
    """Signal to start monitoring (script receives via polling)"""
    return jsonify({'status': 'started', 'type': monitor_type})

@app.route('/api/monitoring/<monitor_type>/stop', methods=['POST'])
def stop_monitoring(monitor_type):
    """Signal to stop monitoring (script receives via polling)"""
    return jsonify({'status': 'stopped', 'type': monitor_type})

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# ============================================================================
# WEBSOCKET EVENTS
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"Client connected: {request.sid}")
    emit('connected', {'data': 'Connected to monitoring server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"Client disconnected: {request.sid}")

@socketio.on('subscribe_alerts')
def handle_subscribe():
    """Subscribe client to alert updates"""
    join_room('alerts')
    emit('subscribed', {'data': 'Subscribed to alerts'})

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 ICU Pain Watcher Backend Server")
    print("=" * 70)
    print(f"✓ API Server: http://localhost:5000/api")
    print(f"✓ WebSocket: ws://localhost:5000")
    print("=" * 70)
    
    # Run Flask-SocketIO server
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
