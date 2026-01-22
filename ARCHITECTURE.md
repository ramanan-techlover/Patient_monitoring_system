# 🏗️ System Architecture & Data Flow

## 📐 High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                    🏥 ICU PAIN WATCHER SYSTEM                        │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    MONITORING SCRIPTS (Python)                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │  Pain Monitor    │  │Agitation Monitor │  │  Audio Monitor   │ │
│  │                  │  │                  │  │                  │ │
│  │ • Facial detect  │  │ • Pose detection │  │ • Transcription  │ │
│  │ • Action Units   │  │ • Head movement  │  │ • Keyword detect │ │
│  │ • Score calc     │  │ • Arm movement   │  │ • Text analysis  │ │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘ │
│           │                     │                     │             │
│           └─────────────────────┼─────────────────────┘             │
│                                 │                                   │
│                 POST /api/*/update (JSON)                          │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │   FLASK BACKEND SERVER     │
                    │                            │
                    │  • REST API (endpoints)    │
                    │  • SocketIO (WebSocket)    │
                    │  • Data storage (in-mem)   │
                    │  • Alert generation        │
                    │  • CORS enabled            │
                    │                            │
                    │  Port: 5000                │
                    └─────────────┬──────────────┘
                                  │
                  ┌───────────────┼───────────────┐
                  │               │               │
         WebSocket Broadcast  REST API        Database
         (Real-time events)   (Historical)    (Optional)
                  │               │               │
        ┌─────────▼──────┐  ┌────▼────────┐    │
        │  REACT FRONTEND │  │   Browser   │    │
        │                │  │   Cache     │    │
        │  • Dashboard   │  │             │    │
        │  • Real-time   │  │ Historical  │    │
        │  • Charts      │  │ data fetch  │    │
        │  • Alerts      │  │             │    │
        │                │  └─────────────┘    │
        │  Port: 3000    │                     │
        └────────────────┘                     │
                                               │
        ┌──────────────────────────────────────┘
        │
        │  (User/Admin)
        │
        ▼
    ┌─────────────────────────────────────┐
    │  ADMIN DASHBOARD                    │
    │                                     │
    │  📊 Main Dashboard                  │
    │  │├─ Key Metrics Cards              │
    │  │├─ Critical Alerts                │
    │  │├─ Real-time Charts               │
    │  │└─ Recent Activity                │
    │                                     │
    │  📈 Detailed Pages                  │
    │  │├─ Pain Analysis                  │
    │  │├─ Agitation Tracking             │
    │  │├─ Audio Transcription            │
    │  │└─ Alert History                  │
    │                                     │
    │  🚨 Alert System                    │
    │  │├─ Real-time notifications        │
    │  │├─ Severity levels                │
    │  │├─ Search & filter                │
    │  │└─ Acknowledgement                │
    │                                     │
    └─────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagram

### Complete Flow: Script → Backend → Frontend

```
┌─────────────────────────────────────────────────────────────────┐
│ MONITORING SCRIPT (Python)                                       │
│                                                                  │
│ import monitoring_client                                        │
│ client = get_monitoring_client()                               │
│ client.start()                                                 │
│                                                                  │
│ # In processing loop:                                          │
│ client.send_pain_data(score, status, au04, au07, au10)        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ POST /api/pain/update
                           │ {
                           │   "score": 2.5,
                           │   "status": "PAIN DETECTED",
                           │   "au04": 0.8,
                           │   "au07": 0.9,
                           │   "au10": 0.8,
                           │   "timestamp": "2026-01-22..."
                           │ }
                           │
                    ┌──────▼──────┐
                    │   INTERNET  │
                    │ (HTTP POST) │
                    └──────┬──────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│ FLASK BACKEND (Python)                                           │
│                                                                  │
│ @app.route('/api/pain/update', methods=['POST'])               │
│ def update_pain_status():                                      │
│     data = request.get_json()                                  │
│     pain_entry = {                                             │
│         'score': data['score'],                                │
│         'status': data['status'],                              │
│         'au04': data['au04'],                                  │
│         'au07': data['au07'],                                  │
│         'au10': data['au10'],                                  │
│         'timestamp': datetime.now().isoformat()                │
│     }                                                           │
│     data_store.pain_history.append(pain_entry)                 │
│                                                                  │
│     # If pain detected, create alert                           │
│     if pain_entry['score'] > 1.5:                             │
│         alert = {...}                                         │
│         data_store.alerts.append(alert)                       │
│         socketio.emit('pain_alert', alert, broadcast=True)    │
│                                                                  │
│     return {'status': 'updated', 'data': pain_entry}          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ WebSocket Broadcast
                           │ Event: 'pain_alert'
                           │ To: All connected clients
                           │
                    ┌──────▼──────────┐
                    │ WEBSOCKET BRIDGE│
                    │  (SocketIO)     │
                    └──────┬──────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│ REACT FRONTEND (JavaScript)                                      │
│                                                                  │
│ // In services/alertService.js                                 │
│ socket.on('pain_alert', (data) => {                           │
│     const alert = {                                            │
│         id: `pain_${Date.now()}`,                              │
│         type: 'PAIN',                                          │
│         severity: data.score > 3 ? 'CRITICAL' : 'WARNING',    │
│         timestamp: new Date(),                                 │
│         message: `Pain Detected: Score ${data.score}`,        │
│         data                                                   │
│     };                                                          │
│     callback(alert); // Update Zustand store                  │
│     toast.error(`🚨 PAIN ALERT: ${data.score}`);              │
│ });                                                             │
│                                                                  │
│ // In store/monitoringStore.js                                │
│ setPainData: (data) => set({                                  │
│     currentPainScore: data.score,                              │
│     painStatus: data.status,                                  │
│     painHistory: [...history, data],                          │
│     painAlert: data                                           │
│ })                                                              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ React re-renders
                           │ Component subscribed to store
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│ BROWSER UI UPDATE                                                │
│                                                                  │
│ ┌────────────────────────────────────────┐                    │
│ │ Dashboard Page                         │                    │
│ ├────────────────────────────────────────┤                    │
│ │ 🚨 Critical Alerts                     │                    │
│ │ ┌──────────────────────────────────┐  │                    │
│ │ │ Pain Alert: 2.50                 │  │                    │
│ │ │ AU04: 0.8 | AU07: 0.9 | AU10: 0.8│ │                    │
│ │ │ [Time: 2026-01-22 14:30:45]      │  │                    │
│ │ └──────────────────────────────────┘  │                    │
│ │                                        │                    │
│ │ Key Metrics: [2.50 / 5.0]             │                    │
│ │                                        │                    │
│ │ ┌─ Pain Graph ──────────────────────┐ │                    │
│ │ │                    ╱╲             │ │                    │
│ │ │                   ╱  ╲  ╱         │ │                    │
│ │ │                  ╱    ╲╱          │ │                    │
│ │ │                                   │ │                    │
│ │ └───────────────────────────────────┘ │                    │
│ │                                        │                    │
│ │ ✓ Toast Notification: 🚨 PAIN ALERT! │                    │
│ │                                        │                    │
│ └────────────────────────────────────────┘                    │
│                                                                  │
│ User sees real-time update < 100ms after script sends data    │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔌 Component Interaction Diagram

```
                           ┌─────────────────┐
                           │  Monitoring     │
                           │  Scripts        │
                           │                 │
                           │ pain_monitor.py │
                           │ agit_monitor.py │
                           │ audio_monitor.py│
                           └────────┬────────┘
                                    │
                        ┌───────────┴────────────┐
                        │                        │
                   HTTP POST            Requires:
                  (JSON data)            • backend/
                        │               • monitoring_
                        │                client.py
                        │
                  ┌─────▼──────┐
                  │   BACKEND  │
                  │   app.py   │
                  │            │
                  │  Flask App │
                  │  SocketIO  │
                  │  CORS      │
                  └─────┬──────┘
                        │
              ┌─────────┼─────────┐
              │         │         │
          REST API  WebSocket  Storage
              │         │         │
              │         │      ┌──▼──┐
              │         │      │ RAM │
              │         │      │(in- │
              │         │      │mem) │
              │         │      └─────┘
              │         │
              │   Broadcast to
              │   all connected
              │   clients
              │         │
        ┌─────▼─────┬───▼──────┐
        │ FRONTEND  │ Browser  │
        │           │ Fetch    │
        │ React App │ Historical
        │           │ data on load
        └─────┬─────┴──────────┘
              │
         ┌────▼─────┐
         │ Dashboard│
         │ Real-time│
         │ Charts   │
         │ Alerts   │
         │ Stats    │
         └──────────┘
```

---

## 📊 State Management Flow

```
React Component
    │
    ├─► useMonitoringStore()  (Zustand)
    │   │
    │   ├─► currentPainScore
    │   ├─► painStatus
    │   ├─► painHistory []
    │   │
    │   ├─► currentAgitationLevel
    │   ├─► agitationStatus
    │   ├─► agitationHistory []
    │   │
    │   ├─► currentAudioTranscript
    │   ├─► detectedKeywords []
    │   ├─► audioHistory []
    │   │
    │   ├─► allAlerts []
    │   ├─► criticalAlerts []
    │   │
    │   └─► Actions:
    │       ├─ setPainData()
    │       ├─ setAgitationData()
    │       ├─ setAudioData()
    │       ├─ addAlert()
    │       ├─ clearAlerts()
    │       └─ initializeAlertSystem()
    │
    └─► subscribes to WebSocket
        updates via alertService
```

---

## 🔐 API Endpoint Hierarchy

```
/api (localhost:5000)
│
├─ /health
│  └─ GET: System health check
│
├─ /pain
│  ├─ /status (GET): Current pain data
│  ├─ /history (GET): Historical pain data
│  └─ /update (POST): Receive pain data from script
│
├─ /agitation
│  ├─ /status (GET): Current agitation level
│  ├─ /history (GET): Historical agitation data
│  └─ /update (POST): Receive agitation data from script
│
├─ /audio
│  ├─ /status (GET): Current audio/transcript
│  ├─ /history (GET): Historical transcript data
│  └─ /update (POST): Receive audio data from script
│
├─ /alerts
│  ├─ GET: All alerts with optional limit
│  ├─ /critical (GET): Critical alerts only
│  └─ /<id>/acknowledge (POST): Mark alert as read
│
└─ /system
   ├─ /status (GET): Overall system status
   └─ /monitoring/<type>
      ├─ /start (POST): Start monitoring
      └─ /stop (POST): Stop monitoring
```

---

## 📈 Performance & Scalability

### Current Design (In-Memory)
```
Data Storage:
├─ pain_history: deque(maxlen=200)
├─ agitation_history: deque(maxlen=200)
├─ audio_history: deque(maxlen=200)
└─ alerts: deque(maxlen=100)

Benefits:
✓ Low latency (< 10ms updates)
✓ Simple implementation
✓ Thread-safe with locks
✓ Auto-cleanup of old data

Limitations:
✗ Data lost on restart
✗ Single-server only
✗ Memory footprint ~5-10MB
```

### Production Upgrade Path
```
Phase 1: Current (In-Memory)
└─ Development & Testing

Phase 2: Database Addition
├─ PostgreSQL for persistence
├─ Redis for caching
└─ Maintains in-memory for speed

Phase 3: Distributed System
├─ Multiple backend servers
├─ Load balancing
├─ Data replication
└─ Horizontal scaling
```

---

## 🎯 Component Dependencies

### Frontend Dependencies
```
React 18
├─ React-Router (navigation)
├─ Axios (API calls)
├─ Socket.io-client (WebSocket)
├─ Chart.js (charts)
├─ Zustand (state)
├─ React-Toastify (notifications)
└─ React-Icons (icons)
```

### Backend Dependencies
```
Flask
├─ Flask-CORS (cross-origin)
├─ Flask-SocketIO (WebSocket)
└─ Requests (HTTP client)
```

### Monitoring Script Dependencies
```
Existing:
├─ OpenAI Whisper
├─ MediaPipe
├─ PyFeat
├─ SoundDevice
├─ OpenCV
└─ Torch

New:
└─ Requests (for API calls)
   (included with Python)
```

---

## 🔄 Update Frequency Recommendations

```
Pain Monitoring:
└─ Send every 10 frames = ~3 fps updates
   (enough to see trends)

Agitation Monitoring:
└─ Send every 5 frames = ~6 fps updates
   (detect movement changes quickly)

Audio Monitoring:
└─ Send only on keywords detected
   (event-driven, not frame-based)

Frontend Updates:
└─ Real-time via WebSocket
   (< 100ms latency)

Historical Data Fetch:
└─ On page load
   (pulls last 100 readings)
```

---

## 📡 Communication Protocols

```
                Script → Backend
                        │
            ┌───────────┴───────────┐
            │                       │
         HTTP POST              WebSocket
         (Initial data)         (Real-time
          Payload: 5KB          events)
          ~20-50ms              <100ms
          Per frame             latency

        Backend → Frontend
                  │
         ┌────────┴────────┐
         │                 │
      WebSocket        REST API
      (Push events)   (Pull history)
      <100ms              ~500ms
      Real-time         On demand
      Updates           Batch loads
```

---

## 🎨 UI Update Pipeline

```
WebSocket Event Received
         ↓
Alert Service processes
         ↓
Store (Zustand) updates
         ↓
Connected components re-render
         ↓
┌────────┴────────────────┐
│                         │
Dashboard Updates    Detail Page Updates
│                    │
├─ Metrics cards    ├─ Charts update
├─ Charts update    ├─ Transcript updates
├─ Alert appears    ├─ Status changes
└─ Toast shows      └─ History refreshes

All within 50-100ms of backend update
```

---

## 🔒 Data Flow Security (TODO for Production)

```
Current (Development):
Script → HTTP → Backend → WS → Frontend
         Plain text

Production (Recommended):
Script → HTTPS → Backend → WSS → Frontend
         Encrypted

Additions needed:
├─ SSL/TLS certificates
├─ API authentication (JWT)
├─ Rate limiting
├─ Input validation
├─ CORS whitelist
└─ Database encryption
```

---

This architecture provides:
- ✅ Real-time monitoring
- ✅ Low latency updates
- ✅ Scalable design
- ✅ Clean separation of concerns
- ✅ Extensible for future features
