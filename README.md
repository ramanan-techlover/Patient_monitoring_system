# 🏥 ICU Pain Watcher - Full Stack Implementation

## 📌 Overview

This is a **complete full-stack monitoring system** for ICU patients that combines:
- **AI-powered pain detection** (facial action units)
- **Motion/agitation detection** (pose estimation)
- **Audio transcription & keyword detection** (Whisper + NLP)
- **Real-time dashboard** (React admin interface)
- **Backend API** (Flask + WebSocket)

All three monitoring systems feed real-time data to a professional admin dashboard with instant alerts.

---

## 🗂️ Project Structure

```
pain-watcher/
│
├── 📁 frontend/                    # React Dashboard
│   ├── public/                     # Static files
│   ├── src/
│   │   ├── components/             # Reusable UI components
│   │   │   ├── Sidebar.js          # Navigation sidebar
│   │   │   ├── AlertCard.js        # Alert display
│   │   │   ├── MonitoringCard.js   # Data visualization
│   │   │   └── StatCard.js         # KPI cards
│   │   ├── pages/                  # Page components
│   │   │   ├── Dashboard.js        # Main overview
│   │   │   ├── PainMonitoring.js   # Pain details
│   │   │   ├── AgitationMonitoring.js # Agitation details
│   │   │   ├── AudioMonitoring.js  # Audio details
│   │   │   └── AlertHistory.js     # Alert logs
│   │   ├── services/
│   │   │   ├── api.js              # REST API client
│   │   │   └── alertService.js     # WebSocket events
│   │   ├── store/
│   │   │   └── monitoringStore.js  # Zustand state management
│   │   ├── styles/                 # CSS files (organized by component)
│   │   └── App.js                  # Main app component
│   ├── package.json                # Dependencies
│   └── .env.example                # Environment variables template
│
├── 📁 backend/                     # Flask API Server
│   ├── app.py                      # Main Flask app with SocketIO
│   ├── monitoring_client.py        # Client for monitoring scripts
│   ├── *_integration.py            # Integration guides for scripts
│   └── requirements.txt            # Python dependencies
│
├── 📝 SETUP_GUIDE.md               # Detailed setup instructions
├── 📖 README.md                    # This file
├── 🚀 start_all.bat                # Quick start (Windows)
├── 🚀 start_all.sh                 # Quick start (Linux/Mac)
│
├── audio_monitor.py                # Audio transcription (existing)
├── pain_monitor.py                 # Pain detection (existing)
├── full_agitation_monitor.py       # Agitation detection (existing)
└── requirements.txt                # Original Python dependencies

```

---

## 🎯 Key Features

### 📊 Admin Dashboard
- **Real-time monitoring** of 3 separate systems
- **Live charts** showing historical trends
- **Critical alert notifications** with severity levels
- **Statistics overview** with KPIs
- **Responsive design** for desktop, tablet, mobile

### 🚨 Alert System
- **Instant notifications** for pain, agitation, keywords
- **Severity levels**: Critical (red), Warning (yellow), Info (blue)
- **Alert history** with filtering and search
- **Alert acknowledgment** for staff workflow

### 📈 Three Monitoring Modules

1. **Pain Detection**
   - Facial Action Units (AU04, AU07, AU10) = Grimace score
   - Real-time pain score display
   - Threshold alerts (> 1.5 = pain warning, > 3.0 = critical)

2. **Agitation Detection**
   - Head movement tracking
   - Arm/limb movement detection
   - Agitation level meter (0-100)
   - Critical threshold at level > 20

3. **Audio Transcription**
   - Real-time speech-to-text (OpenAI Whisper)
   - Keyword detection (help, pain, nurse, emergency, etc.)
   - Transcript history
   - Keyword frequency analysis

---

## ⚡ Quick Start

### Prerequisites
- **Node.js 14+** (for React)
- **Python 3.8+** (for monitoring scripts)
- **GPU** (optional, recommended for AI models)

### 1️⃣ Install Dependencies

```bash
# Frontend
cd frontend
npm install

# Backend
cd ../backend
pip install -r requirements.txt

# Existing monitoring scripts (if not already installed)
cd ..
pip install -r requirements.txt
```

### 2️⃣ Start All Components

**Windows:**
```bash
start_all.bat
```

**Linux/Mac:**
```bash
bash start_all.sh
```

**Manual (3 Terminals):**
```bash
# Terminal 1: Backend
cd backend
python app.py

# Terminal 2: Frontend
cd frontend
npm start

# Terminal 3: Monitoring Scripts
python audio_monitor.py
python pain_monitor.py
python full_agitation_monitor.py
```

### 3️⃣ Access Dashboard
- **Dashboard**: http://localhost:3000
- **API**: http://localhost:5000/api
- **WebSocket**: ws://localhost:5000

---

## 🔌 Integration with Existing Scripts

Each monitoring script needs to send data to the backend. Three options:

### Option A: Minimal Changes (Recommended)
Add these lines to each script:

**pain_monitor.py:**
```python
import sys
sys.path.insert(0, './backend')
from monitoring_client import get_monitoring_client

client = get_monitoring_client()
client.start()

# In main loop, after calculating pain:
if frame_count % 10 == 0:
    client.send_pain_data(
        score=current_pain_score,
        status=status_text,
        au04=au4, au07=au7, au10=au10
    )
```

**full_agitation_monitor.py:**
```python
import sys
sys.path.insert(0, './backend')
from monitoring_client import get_monitoring_client

client = get_monitoring_client()
client.start()

# In main loop:
if frame_count % 5 == 0:
    client.send_agitation_data(
        level=agitation_counter,
        status=status_text,
        head_speed=head_speed,
        arm_speed=arm_speed
    )
```

**audio_monitor.py:**
```python
import sys
sys.path.insert(0, './backend')
from monitoring_client import get_monitoring_client

client = get_monitoring_client()
client.start()

# When keywords detected:
client.send_audio_data(
    text=text,
    keywords=detected_keywords
)
```

### Option B: Use Integration Templates
See `backend/*_integration.py` files for complete examples.

---

## 📡 API Documentation

### Endpoints

**Health**
```
GET /api/health
```

**Pain Monitoring**
```
GET    /api/pain/status              # Current status
GET    /api/pain/history?limit=100   # Historical data
POST   /api/pain/update              # Send data from script
```

**Agitation Monitoring**
```
GET    /api/agitation/status
GET    /api/agitation/history?limit=100
POST   /api/agitation/update
```

**Audio Monitoring**
```
GET    /api/audio/status
GET    /api/audio/history?limit=100
POST   /api/audio/update
```

**Alerts**
```
GET    /api/alerts?limit=50          # All alerts
GET    /api/alerts/critical          # Critical only
POST   /api/alerts/<id>/acknowledge  # Mark as read
```

**System**
```
GET    /api/system/status            # Overall status
POST   /api/monitoring/<type>/start   # Start monitoring
POST   /api/monitoring/<type>/stop    # Stop monitoring
```

### WebSocket Events

```javascript
// Real-time alerts
socket.on('pain_alert', (alert) => { ... })
socket.on('agitation_alert', (alert) => { ... })
socket.on('audio_alert', (alert) => { ... })
```

---

## 🎨 Dashboard Pages

### 1. Main Dashboard
```
[Top] Critical Alerts Bar
[Left] Key Metrics (4 cards)
[Right] Real-time Charts (Pain + Agitation)
[Bottom] Recent Activity Feed
```

### 2. Pain Monitoring
```
Current Score Display
Graph: Pain Score Over Time
Action Unit Analysis (AU04, AU07, AU10)
Detailed Statistics
```

### 3. Agitation Monitoring
```
Agitation Level Indicator
Graph: Movement Over Time
Head/Arm Movement Analysis
Threshold Information
```

### 4. Audio Monitoring
```
Current Transcript
Detected Keywords (Live)
Keyword Frequency Stats
Transcript History (20+ entries)
```

### 5. Alert History
```
Statistics Overview
Filters (Type, Severity)
Searchable Alert Table
Detailed Alert Expansion
```

---

## ⚙️ Configuration

### Environment Variables

**Frontend (.env):**
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_SOCKET_URL=http://localhost:5000
REACT_APP_ENV=development
```

**Backend (set in app.py):**
```python
FLASK_ENV='development'
FLASK_DEBUG=True
API_PORT=5000
```

### Adjusting Thresholds

**Pain Threshold** (backend/app.py):
```python
PAIN_WARNING = 1.5
PAIN_CRITICAL = 3.0
```

**Agitation Threshold** (backend/app.py):
```python
AGITATION_WARNING = 10
AGITATION_CRITICAL = 20
```

**Keywords** (audio_monitor.py):
```python
KEYWORDS = ["help", "nurse", "pain", "doctor", "emergency", ...]
```

---

## 🧪 Testing

### Test API Connection
```bash
curl http://localhost:5000/api/health
```

### Simulate Pain Alert
```bash
curl -X POST http://localhost:5000/api/pain/update \
  -H "Content-Type: application/json" \
  -d '{"score": 3.5, "status": "PAIN DETECTED", "au04": 0.8, "au07": 0.9, "au10": 1.8}'
```

### Simulate Agitation Alert
```bash
curl -X POST http://localhost:5000/api/agitation/update \
  -H "Content-Type: application/json" \
  -d '{"level": 25, "status": "CRITICAL: PATIENT THRASHING", "head_speed": 0.05, "arm_speed": 0.08}'
```

### Simulate Audio Alert
```bash
curl -X POST http://localhost:5000/api/audio/update \
  -H "Content-Type: application/json" \
  -d '{"text": "Help me please!", "keywords": ["help", "pain"]}'
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 5000 already in use | `netstat -ano \| findstr :5000` then kill the process |
| npm not found | Install Node.js from https://nodejs.org |
| Python not found | Install Python from https://www.python.org |
| Backend not connecting | Check firewall, verify port 5000 is open |
| No real-time updates | Check WebSocket in browser DevTools Network tab |
| Data not appearing | Verify integration code was added to monitoring scripts |
| CORS errors | Ensure Flask-CORS is installed: `pip install Flask-CORS` |

---

## 📊 Data Flow

```
Monitoring Script → POST /api/*/update → Flask Backend → WebSocket → React Dashboard
                                              ↓
                                        In-Memory Storage
                                              ↓
                                        GET /api/*/history
```

---

## 🚀 Deployment

### Local Network
1. Start backend with `0.0.0.0:5000`
2. Update frontend `.env` to backend IP
3. Access from any device on network

### Production
1. Use database (PostgreSQL/MongoDB) instead of in-memory storage
2. Implement authentication/authorization
3. Use SSL/TLS (HTTPS + WSS)
4. Deploy with Docker or cloud platform
5. Add logging and monitoring

---

## 📝 Notes

- Data is **stored in-memory** (max 200 readings per monitor, 100 alerts)
- Data **persists only while backend is running**
- For production, implement **database persistence**
- GPU **recommended** for real-time inference
- **CPU fallback** works but slower

---

## 📞 Support

For issues or questions:
1. Check `SETUP_GUIDE.md` for detailed instructions
2. Review integration files in `backend/`
3. Check browser console for frontend errors
4. Check terminal output for backend errors

---

## 📄 License

This project is part of MHA Pain Watcher initiative.

---

**Last Updated:** January 22, 2026
**Version:** 1.0.0
