# Pain Watcher - Full Stack Setup Guide

## 🏥 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                          │
│  (Dashboard, Real-time Charts, Alerts)                      │
│  Port: 3000 | npm start                                     │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API + WebSocket
                         │ (http://localhost:5000)
┌────────────────────────▼────────────────────────────────────┐
│              Backend (Flask + SocketIO)                      │
│  (API Server, Alert Handling, Data Storage)                 │
│  Port: 5000 | python app.py                                 │
└────────────────────────▲────────────────────────────────────┘
                         │ POST /api/*/update
                         │
      ┌──────────────────┼──────────────────┐
      │                  │                  │
┌─────▼──────┐ ┌─────────▼──┐ ┌────────────▼───┐
│ Audio      │ │ Pain       │ │ Agitation      │
│ Monitor    │ │ Monitor    │ │ Monitor        │
│ (Script)   │ │ (Script)   │ │ (Script)       │
└────────────┘ └────────────┘ └────────────────┘
```

## 📋 Installation Steps

### 1. Frontend Setup

```bash
cd frontend
npm install
```

**Required packages:**
- react
- react-router-dom
- axios
- chart.js
- react-chartjs-2
- socket.io-client
- tailwindcss
- react-icons
- react-toastify
- zustand

### 2. Backend Setup

```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt
```

**Required packages:**
- Flask
- Flask-CORS
- Flask-SocketIO
- python-socketio
- requests

### 3. Monitoring Scripts

The existing monitoring scripts (audio_monitor.py, pain_monitor.py, full_agitation_monitor.py) need to be updated to send data to the backend.

## 🚀 Running the Application

### Terminal 1: Start Backend API Server
```bash
cd backend
python app.py
```
✓ Backend running at: http://localhost:5000
✓ API endpoints available at: http://localhost:5000/api

### Terminal 2: Start Frontend
```bash
cd frontend
npm start
```
✓ Frontend running at: http://localhost:3000
✓ Auto-opens in browser

### Terminal 3+: Start Monitoring Scripts
```bash
# Run each in separate terminals
python audio_monitor.py
python pain_monitor.py
python full_agitation_monitor.py
```

## 📡 Integration Steps

### Option A: Quick Integration (Using Pre-built Files)

1. **For Pain Monitor:**
   ```python
   # Add to pain_monitor.py after imports:
   sys.path.insert(0, './backend')
   from monitoring_client import get_monitoring_client
   
   monitoring_client = get_monitoring_client()
   monitoring_client.start()
   
   # In main loop, after calculating pain score:
   if frame_count % 10 == 0:
       monitoring_client.send_pain_data(
           score=current_pain_score,
           status=status_text,
           au04=au4,
           au07=au7,
           au10=au10,
       )
   ```

2. **For Agitation Monitor:**
   ```python
   # Similar pattern - add at top:
   sys.path.insert(0, './backend')
   from monitoring_client import get_monitoring_client
   
   monitoring_client = get_monitoring_client()
   monitoring_client.start()
   
   # In main loop:
   if frame_count % 5 == 0:
       monitoring_client.send_agitation_data(
           level=agitation_counter,
           status=status_text,
           head_speed=head_speed,
           arm_speed=arm_speed,
       )
   ```

3. **For Audio Monitor:**
   ```python
   # Same pattern - add at top:
   sys.path.insert(0, './backend')
   from monitoring_client import get_monitoring_client
   
   monitoring_client = get_monitoring_client()
   monitoring_client.start()
   
   # In queue processing loop:
   if detected_keywords:
       monitoring_client.send_audio_data(
           text=text,
           keywords=detected_keywords,
       )
   ```

### Option B: Complete Integration (Full Modified Versions)

Use the provided integration files:
- `backend/pain_monitor_integration.py`
- `backend/agitation_monitor_integration.py`
- `backend/audio_monitor_integration.py`

These contain detailed examples of where and how to add the monitoring_client calls.

## 🔌 API Endpoints

### Pain Monitoring
- `GET /api/pain/status` - Get current pain status
- `GET /api/pain/history?limit=100` - Get pain history
- `POST /api/pain/update` - Send pain data (called by script)

### Agitation Monitoring
- `GET /api/agitation/status` - Get current agitation status
- `GET /api/agitation/history?limit=100` - Get agitation history
- `POST /api/agitation/update` - Send agitation data (called by script)

### Audio Monitoring
- `GET /api/audio/status` - Get current audio status
- `GET /api/audio/history?limit=100` - Get audio history
- `POST /api/audio/update` - Send audio data (called by script)

### Alerts
- `GET /api/alerts?limit=50` - Get all alerts
- `GET /api/alerts/critical` - Get critical alerts only
- `POST /api/alerts/<id>/acknowledge` - Mark alert as acknowledged

### System
- `GET /api/system/status` - Get overall system status
- `GET /api/health` - Health check

## 🔴 WebSocket Events

The frontend connects to the backend via WebSocket for real-time updates:

```javascript
// Pain alert
socket.on('pain_alert', (alert) => {
  // Handle pain alert
})

// Agitation alert
socket.on('agitation_alert', (alert) => {
  // Handle agitation alert
})

// Audio alert
socket.on('audio_alert', (alert) => {
  // Handle audio alert
})
```

## 📊 Dashboard Features

### Main Dashboard
- Real-time monitoring of all three systems
- Critical alerts display
- Key metrics cards
- Recent activity feed

### Pain Monitoring Page
- Detailed pain score graph
- AU (Action Unit) values: AU04, AU07, AU10
- Historical trends
- Status indicators

### Agitation Monitoring Page
- Agitation level timeline
- Head and arm movement tracking
- Critical threshold indicators
- Movement analysis

### Audio Monitoring Page
- Real-time transcription display
- Keyword detection highlighting
- Transcript history
- Keyword frequency statistics

### Alert History
- Filterable alert table
- Statistics overview
- Critical/warning severity badges
- Detailed alert information

## 🎯 Configuration

### Backend (.env)
```
FLASK_ENV=development
FLASK_DEBUG=True
API_PORT=5000
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_SOCKET_URL=http://localhost:5000
```

## ⚙️ Adjusting Sensitivities

### Pain Threshold
In backend/app.py:
```python
if pain_entry['score'] > 1.5:  # Adjust this value
    alert = {...}
```

### Agitation Threshold
In backend/app.py:
```python
if agitation_entry['level'] > 10:  # Adjust warning threshold
    # and > 20 for critical
```

### Keyword Sensitivity
In audio_monitor.py, adjust:
```python
KEYWORDS = ["help", "nurse", "pain", "doctor", "emergency", ...]  # Add/remove keywords
```

## 🧪 Testing the System

1. **Start all components:**
   ```bash
   # Terminal 1
   cd backend && python app.py
   
   # Terminal 2
   cd frontend && npm start
   
   # Terminal 3+
   python audio_monitor.py
   python pain_monitor.py
   python full_agitation_monitor.py
   ```

2. **Check API:**
   ```bash
   curl http://localhost:5000/api/health
   ```

3. **Simulate alerts:**
   ```bash
   curl -X POST http://localhost:5000/api/pain/update \
     -H "Content-Type: application/json" \
     -d '{"score": 3.5, "status": "PAIN DETECTED", "au04": 0.8, "au07": 0.9, "au10": 1.8}'
   ```

4. **View dashboard:**
   - Open http://localhost:3000 in browser
   - Check for alerts in real-time

## 🐛 Troubleshooting

### Backend not connecting
- Check if port 5000 is available: `netstat -ano | findstr :5000`
- Check firewall settings
- Verify Flask is installed: `pip list | grep Flask`

### Frontend not updating
- Check browser console for errors
- Verify WebSocket connection in Network tab
- Check if backend is running: `curl http://localhost:5000/api/health`

### No data appearing
- Verify monitoring scripts are running
- Check backend logs for POST requests
- Verify integration code was added correctly
- Test API directly: `curl http://localhost:5000/api/pain/status`

## 📝 Notes

- All historical data is stored in-memory (max 200 items per monitor)
- Alerts are stored in-memory (max 100)
- Data persists only while backend is running
- For production, implement database storage

## 📚 File Structure

```
pain-watcher/
├── frontend/                 # React Dashboard
│   ├── public/
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API calls
│   │   ├── store/            # Zustand state management
│   │   ├── styles/           # CSS files
│   │   └── App.js
│   └── package.json
│
├── backend/                  # Flask Backend
│   ├── app.py               # Main Flask app
│   ├── monitoring_client.py  # Integration client
│   ├── *_integration.py     # Integration guides
│   └── requirements.txt
│
├── audio_monitor.py         # Audio monitoring script
├── pain_monitor.py          # Pain detection script
├── full_agitation_monitor.py # Agitation detection script
└── requirements.txt         # Python dependencies

```
