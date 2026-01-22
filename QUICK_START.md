# Quick Start Guide - Running the Pain Watcher System

## Prerequisites Check

Run this first to verify your camera and microphone:
```bash
python test_camera_audio.py
```

## Starting the System

You need **3 terminals** running simultaneously:

### Terminal 1: Backend API Server
```bash
cd backend
python app.py
```
Wait until you see: `✓ API Server: http://localhost:5000/api`

### Terminal 2: Frontend Dashboard  
```bash
cd frontend
npm start
```
Wait until browser opens at: `http://localhost:3000`

### Terminal 3: Run ONE monitoring script at a time

**Option A - Pain Monitor:**
```bash
python pain_monitor.py
```

**Option B - Agitation Monitor:**
```bash
python full_agitation_monitor.py
```

**Option C - Audio Monitor:**
```bash
python audio_monitor.py
```

## What You Should See

1. **Backend Terminal**: Shows incoming data from monitoring scripts
2. **Frontend Dashboard**: Updates in real-time with metrics and alerts
3. **Monitoring Script**: Shows camera/audio feed and detection results

## Troubleshooting

### Camera Not Working
- Close any other apps using the camera (Zoom, Teams, etc.)
- Check camera permissions in Windows Settings
- Try unplugging and replugging the camera

### Audio Not Working
- Check microphone permissions in Windows Settings
- Make sure correct microphone is selected as default
- Speak clearly near the microphone

### Dashboard Not Updating
- Make sure backend is running (Terminal 1)
- Check browser console (F12) for connection status
- Verify "✓ Connected to monitoring system" shows in dashboard

### Integration Errors
- Make sure you're running from the main `pain-watcher` directory
- Check that `backend/monitoring_client.py` exists
- Verify backend is running before starting monitoring scripts

## Testing Data Flow

1. Start backend and frontend
2. Run pain monitor
3. Make a pain face (frown, squint) at the camera
4. Watch the dashboard update with pain score
5. Check "Pain Monitor" page for detailed metrics

## Tips

- **Pain Monitor**: Works best with good lighting and face clearly visible
- **Agitation Monitor**: Needs full upper body in frame  
- **Audio Monitor**: Speak keywords like "help", "pain", "nurse"
- Dashboard updates every few seconds (not instant)
- Press 'q' in monitoring script window to quit cleanly
