# 🔧 Step-by-Step Implementation Guide

## Phase 1: Backend Setup ✅

### Step 1: Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

**Verify installation:**
```bash
python -c "import flask; import flask_socketio; print('✓ Backend dependencies OK')"
```

### Step 2: Test Backend Server
```bash
python app.py
```

You should see:
```
======================================================================
🚀 ICU Pain Watcher Backend Server
======================================================================
✓ API Server: http://localhost:5000/api
✓ WebSocket: ws://localhost:5000
======================================================================
```

### Step 3: Test API Endpoints
Open new terminal and run:

```bash
# Health check
curl http://localhost:5000/api/health

# Get pain status
curl http://localhost:5000/api/pain/status

# Get system status
curl http://localhost:5000/api/system/status
```

Expected responses:
```json
{"status": "healthy", "timestamp": "..."}
{"score": 0, "status": "COMFORT", "timestamp": null}
{"pain": {...}, "agitation": {...}, "audio": {...}, "stats": {...}}
```

---

## Phase 2: Frontend Setup ✅

### Step 1: Install Frontend Dependencies
```bash
cd frontend
npm install
```

**Verify installation:**
```bash
npm list react react-router-dom socket.io-client
```

### Step 2: Create .env File
```bash
cp .env.example .env
```

Content should be:
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_SOCKET_URL=http://localhost:5000
REACT_APP_ENV=development
```

### Step 3: Start Frontend
```bash
npm start
```

You should see:
```
On Your Network: http://xxx.xxx.xxx.xxx:3000/
Compiled successfully!
You can now view pain-watcher-dashboard in the browser.
```

Frontend will auto-open at: http://localhost:3000

---

## Phase 3: Backend-Frontend Connection ✅

### Step 1: Verify WebSocket Connection

1. **Open Dashboard** → http://localhost:3000
2. **Open Browser DevTools** → F12 → Console
3. **Look for:**
   ```
   ✓ Connected to monitoring server
   ```

### Step 2: Send Test Data to Backend

In a terminal, run:
```bash
curl -X POST http://localhost:5000/api/pain/update \
  -H "Content-Type: application/json" \
  -d '{
    "score": 2.5,
    "status": "PAIN DETECTED",
    "au04": 0.8,
    "au07": 0.9,
    "au10": 0.8
  }'
```

### Step 3: Verify Dashboard Updates

1. **Check Console** → Should show green success message
2. **Check Dashboard** → 
   - Pain score should show "2.50"
   - Status should show "PAIN DETECTED"
   - Alert should appear in recent activity
3. **Check Alerts Page** → New alert should be listed

---

## Phase 4: Monitoring Scripts Integration ✅

### Step 1: Integrate Pain Monitor

**Edit: pain_monitor.py**

Add after imports:
```python
import sys
sys.path.insert(0, './backend')
from monitoring_client import get_monitoring_client

# Initialize client
monitoring_client = get_monitoring_client()
monitoring_client.start()
```

Find this section (around line 70):
```python
if detected is not None and len(detected) > 0:
    au4 = detected["AU04"].values[0]
    au7 = detected["AU07"].values[0]
    au10 = detected["AU10"].values[0]
    current_pain_score = au4 + au7 + au10
```

Add after `current_pain_score = au4 + au7 + au10`:
```python
    # SEND TO BACKEND (every 10 frames to reduce overhead)
    if frame_count % 10 == 0:
        monitoring_client.send_pain_data(
            score=current_pain_score,
            status=status_text,
            au04=au4,
            au07=au7,
            au10=au10,
        )
```

**Test:**
```bash
python pain_monitor.py
```

Check dashboard:
- ✓ Pain score updates in real-time
- ✓ Graph shows trend
- ✓ Alerts trigger for high scores

### Step 2: Integrate Agitation Monitor

**Edit: full_agitation_monitor.py**

Add after imports:
```python
import sys
sys.path.insert(0, './backend')
from monitoring_client import get_monitoring_client

monitoring_client = get_monitoring_client()
monitoring_client.start()
```

Find section around line 120 where `agitation_counter` is updated. Add:
```python
    # SEND TO BACKEND (every 5 frames)
    if frame_count % 5 == 0:
        monitoring_client.send_agitation_data(
            level=agitation_counter,
            status=status_text,
            head_speed=head_speed,
            arm_speed=arm_speed,
        )
```

**Test:**
```bash
python full_agitation_monitor.py
```

Check dashboard:
- ✓ Agitation level updates
- ✓ Graph shows movement trend
- ✓ Critical alerts at level > 20

### Step 3: Integrate Audio Monitor

**Edit: audio_monitor.py**

Add after imports:
```python
import sys
sys.path.insert(0, './backend')
from monitoring_client import get_monitoring_client

monitoring_client = get_monitoring_client()
monitoring_client.start()
```

Find section in main loop where queue is processed (around line 180):
```python
try:
    text = audio_queue.get(timeout=1)
    detected_keywords = [kw for kw in KEYWORDS if kw in text]
    
    # ADD THIS:
    monitoring_client.send_audio_data(
        text=text,
        keywords=detected_keywords,
    )
```

**Test:**
```bash
python audio_monitor.py
```

Speak keywords like "help", "pain", "nurse"

Check dashboard:
- ✓ Transcript appears
- ✓ Keywords detected and highlighted
- ✓ Alerts trigger on keyword detection

---

## Phase 5: Full System Test ✅

### Checklist: All Components Running

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
# Should show: ✓ API Server: http://localhost:5000/api
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
# Should show: Compiled successfully!
```

**Terminal 3 - Pain Monitor:**
```bash
python pain_monitor.py
# Should show: Listening on '[camera name]'...
```

**Terminal 4 - Agitation Monitor:**
```bash
python full_agitation_monitor.py
# Should show: Full-Body Agitation Monitor Active...
```

**Terminal 5 - Audio Monitor:**
```bash
python audio_monitor.py
# Should show: Listening on '[microphone name]'...
```

### Dashboard Verification

1. **Open:** http://localhost:3000
2. **Should see:**
   - ✓ Connected status (green indicator)
   - ✓ Real-time metrics updating
   - ✓ Charts showing trends
   - ✓ No errors in console

### Test Each Monitor

#### Pain Test:
1. Make pain faces (grimace, frown, squint)
2. Watch pain score increase
3. Check alerts for pain detection

#### Agitation Test:
1. Move head side-to-side
2. Raise and lower arms
3. Watch agitation level increase
4. Verify alert at level > 20

#### Audio Test:
1. Speak clearly: "I need help"
2. Listen for transcription
3. Check keywords detected
4. Verify "help" keyword highlighted

---

## Troubleshooting Matrix

### Backend Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Port 5000 in use | Another app using port | Kill process or change port |
| Import error (Flask) | Dependencies not installed | `pip install -r requirements.txt` |
| WebSocket errors | CORS issue | Check Flask-CORS is installed |
| API returns 404 | Wrong URL or endpoint | Check URL format in browser |

### Frontend Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| npm: command not found | Node.js not installed | Install from nodejs.org |
| Module not found | Dependencies missing | `npm install` in frontend dir |
| Blank page | React error | Check browser console (F12) |
| No real-time updates | WebSocket not connecting | Check backend is running on 5000 |

### Integration Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| `ModuleNotFoundError: monitoring_client` | Wrong path | Verify `sys.path.insert(0, './backend')` |
| Data not appearing | send_* not called | Add code in main loop |
| Connection refused | Backend not running | Start backend first |
| Alerts not triggering | Threshold too high | Lower thresholds in backend/app.py |

---

## Advanced Troubleshooting

### Check Backend Logs
```bash
# In backend terminal, you'll see:
✓ Data sent to pain/update
✓ Data sent to agitation/update
✓ Data sent to audio/update
```

### Check Network Traffic
1. Open DevTools → Network tab
2. Look for WebSocket (ws) connections
3. Watch for real-time messages

### Check API Manually
```bash
# Get current pain status
curl http://localhost:5000/api/pain/status | python -m json.tool

# Get all alerts
curl http://localhost:5000/api/alerts | python -m json.tool

# Get system overview
curl http://localhost:5000/api/system/status | python -m json.tool
```

### Browser Console Errors

**CORS Error:**
```
Access to XMLHttpRequest blocked by CORS policy
```
→ Restart backend with `python app.py`

**WebSocket Connection Failed:**
```
WebSocket connection to 'ws://localhost:5000' failed
```
→ Verify backend running, check port 5000

**Blank State:**
```
Cannot read property 'map' of undefined
```
→ Wait for initial data, check backend sending data

---

## Performance Tips

### Reduce Network Overhead
In monitoring scripts, use async sending:
```python
monitoring_client.send_pain_data(
    score=current_pain_score,
    status=status_text,
    au04=au4, au07=au7, au10=au10,
    async_send=True  # Queue for background sending
)
```

### Reduce Frame Processing
Send every Nth frame:
```python
if frame_count % 10 == 0:  # Every 10 frames = ~3 FPS updates
    monitoring_client.send_pain_data(...)
```

### Monitor Resource Usage
```bash
# Terminal: Watch memory usage
watch -n 1 'ps aux | grep python'
```

---

## Final Verification

Run this checklist before deployment:

- [ ] Backend starts without errors
- [ ] Frontend builds successfully
- [ ] Dashboard loads at http://localhost:3000
- [ ] WebSocket connection shows "✓ Connected"
- [ ] Pain monitor sends data (visible in dashboard)
- [ ] Agitation monitor sends data (visible in dashboard)
- [ ] Audio monitor sends data (visible in dashboard)
- [ ] Alerts trigger for critical events
- [ ] Alert history logs all events
- [ ] No errors in browser console (F12)
- [ ] No errors in backend terminal
- [ ] All graphs update smoothly
- [ ] Responsive design works on mobile (F12 → toggle device)

---

## Success! 🎉

If all checks pass, your **Pain Watcher system is ready for use!**

**Next Steps:**
1. Train staff on dashboard usage
2. Configure monitoring thresholds for your ICU
3. Set up alerts/notifications for nursing station
4. Monitor system reliability in test environment
5. Deploy to production when confident

---

**Questions?** Check the README.md or SETUP_GUIDE.md
