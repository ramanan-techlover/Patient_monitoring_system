# ⚡ Quick Reference Card

## 🚀 Start All Components

### Windows
```bash
start_all.bat
```

### Linux/Mac
```bash
bash start_all.sh
```

### Manual (3 terminals)
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

---

## 🌐 Access Points

| Component | URL | Status |
|-----------|-----|--------|
| Dashboard | http://localhost:3000 | React App |
| API | http://localhost:5000/api | Flask |
| WebSocket | ws://localhost:5000 | SocketIO |
| Health | http://localhost:5000/api/health | Health Check |

---

## 📦 Installation Checklist

- [ ] Frontend: `cd frontend && npm install`
- [ ] Backend: `cd backend && pip install -r requirements.txt`
- [ ] Existing: `pip install -r requirements.txt` (already have)

---

## 🔌 Integration Code (3 scripts)

### Pain Monitor (pain_monitor.py)
```python
# After imports:
sys.path.insert(0, './backend')
from monitoring_client import get_monitoring_client
client = get_monitoring_client()
client.start()

# In main loop (after calculating pain):
if frame_count % 10 == 0:
    client.send_pain_data(current_pain_score, status_text, au4, au7, au10)
```

### Agitation Monitor (full_agitation_monitor.py)
```python
# After imports:
sys.path.insert(0, './backend')
from monitoring_client import get_monitoring_client
client = get_monitoring_client()
client.start()

# In main loop (every 5 frames):
if frame_count % 5 == 0:
    client.send_agitation_data(agitation_counter, status_text, head_speed, arm_speed)
```

### Audio Monitor (audio_monitor.py)
```python
# After imports:
sys.path.insert(0, './backend')
from monitoring_client import get_monitoring_client
client = get_monitoring_client()
client.start()

# In queue loop (when keywords detected):
client.send_audio_data(text, detected_keywords)
```

---

## 🧪 Test API Endpoints

```bash
# Health
curl http://localhost:5000/api/health

# Pain Status
curl http://localhost:5000/api/pain/status

# Agitation Status
curl http://localhost:5000/api/agitation/status

# Audio Status
curl http://localhost:5000/api/audio/status

# System Status
curl http://localhost:5000/api/system/status

# All Alerts
curl http://localhost:5000/api/alerts

# Critical Alerts
curl http://localhost:5000/api/alerts/critical
```

---

## 📤 Test Sending Data

```bash
# Send Pain Data
curl -X POST http://localhost:5000/api/pain/update \
  -H "Content-Type: application/json" \
  -d '{"score": 2.5, "status": "PAIN DETECTED", "au04": 0.8, "au07": 0.9, "au10": 0.8}'

# Send Agitation Data
curl -X POST http://localhost:5000/api/agitation/update \
  -H "Content-Type: application/json" \
  -d '{"level": 15, "status": "Warning: Restless", "head_speed": 0.03, "arm_speed": 0.04}'

# Send Audio Data
curl -X POST http://localhost:5000/api/audio/update \
  -H "Content-Type: application/json" \
  -d '{"text": "I need help", "keywords": ["help"]}'
```

---

## 📊 Dashboard Pages

| Page | URL | Purpose |
|------|-----|---------|
| Main | http://localhost:3000 | Overview & metrics |
| Pain | http://localhost:3000/pain | Detailed pain analysis |
| Agitation | http://localhost:3000/agitation | Movement tracking |
| Audio | http://localhost:3000/audio | Transcription & keywords |
| Alerts | http://localhost:3000/alerts | Alert history & logs |

---

## 🎯 Thresholds (in backend/app.py)

```python
# Pain
PAIN_WARNING = 1.5   # Alert when > 1.5
PAIN_CRITICAL = 3.0  # Critical when > 3.0

# Agitation
AGITATION_WARNING = 10   # Alert when > 10
AGITATION_CRITICAL = 20  # Critical when > 20

# Keywords (in audio_monitor.py)
KEYWORDS = ["help", "nurse", "pain", "doctor", "emergency", ...]
```

---

## 🐛 Quick Troubleshooting

| Problem | Fix |
|---------|-----|
| Port 5000 in use | Kill process: `lsof -ti:5000 \| xargs kill` |
| npm not found | Install Node.js from nodejs.org |
| Python not found | Install Python from python.org |
| Module not found | Run: `cd frontend && npm install` |
| Connection refused | Start backend: `cd backend && python app.py` |
| No data in dashboard | Add integration code to monitoring scripts |
| CORS error | Ensure Flask-CORS installed: `pip install Flask-CORS` |

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `backend/app.py` | Flask API server |
| `backend/monitoring_client.py` | Python client |
| `frontend/src/App.js` | Main React app |
| `frontend/src/store/monitoringStore.js` | State management |
| `frontend/src/services/api.js` | API calls |
| `SETUP_GUIDE.md` | Installation guide |
| `IMPLEMENTATION_GUIDE.md` | Integration steps |

---

## 🔌 Monitoring Client API

```python
from monitoring_client import get_monitoring_client

client = get_monitoring_client()
client.start()  # Start background thread

# Send data
client.send_pain_data(score, status, au04, au07, au10)
client.send_agitation_data(level, status, head_speed, arm_speed)
client.send_audio_data(text, keywords)

# Get status
status = client.get_status('pain')

# Health check
if client.health_check():
    print("Backend is running")
```

---

## 🎨 Color Indicators

| Color | Meaning | Example |
|-------|---------|---------|
| 🟢 Green | Normal/Safe | Calm, Comfortable |
| 🟡 Yellow | Warning | Restless, Warning level |
| 🔴 Red | Critical | Pain Detected, Critical level |
| 🔵 Blue | Information | Audio keywords |

---

## 📊 Real-time Chart Updates

- **Pain**: Updates every 30 frames (from integration)
- **Agitation**: Updates every 15 frames (from integration)
- **Audio**: Updates on keyword detection
- **Dashboard**: Refreshes on WebSocket event

---

## 🔄 Data Flow

```
Monitoring Script
    ↓ POST /api/*/update
Flask Backend
    ↓ Store data + WebSocket broadcast
In-Memory Storage
    ↓ Emit to connected clients
React Frontend
    ↓ Update charts + alerts
Admin Dashboard
```

---

## 📱 Responsive Breakpoints

- Desktop: 1400px+
- Tablet: 768px - 1399px
- Mobile: < 768px

---

## 🔐 Environment Variables

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_SOCKET_URL=http://localhost:5000
REACT_APP_ENV=development
```

### Backend (in code)
```python
FLASK_ENV='development'
FLASK_DEBUG=True
API_PORT=5000
```

---

## 📞 Resources

- **Setup**: SETUP_GUIDE.md
- **Implementation**: IMPLEMENTATION_GUIDE.md
- **Project Info**: PROJECT_SUMMARY.md
- **ReadMe**: README.md

---

## ✅ Verification Checklist

- [ ] Backend running on 5000
- [ ] Frontend running on 3000
- [ ] Dashboard loads without errors
- [ ] WebSocket connected (green indicator)
- [ ] API responding to curl requests
- [ ] Pain script sends data
- [ ] Agitation script sends data
- [ ] Audio script sends data
- [ ] Alerts appearing in dashboard
- [ ] Charts updating in real-time
- [ ] Responsive design working

---

## 🚀 Ready to Go!

Follow **IMPLEMENTATION_GUIDE.md** for complete step-by-step setup.

**Questions?** Check PROJECT_SUMMARY.md or README.md
