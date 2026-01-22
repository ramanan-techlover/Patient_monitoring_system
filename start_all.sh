#!/bin/bash
# ======================================================================
# Pain Watcher - Quick Start Script (Linux/Mac)
# Run all components with one command
# ======================================================================

echo ""
echo "======================================================================"
echo "  🏥 ICU Pain Watcher - System Startup"
echo "======================================================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install from https://nodejs.org"
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install from https://www.python.org"
    exit 1
fi

echo "✓ Node.js found:"
node --version
echo ""
echo "✓ Python found:"
python --version
echo ""

# Start Backend
echo "Starting Backend..."
cd backend
python app.py &
BACKEND_PID=$!
sleep 2

# Start Frontend
echo "Starting Frontend..."
cd ../frontend
npm start &
FRONTEND_PID=$!
sleep 2

echo ""
echo "======================================================================"
echo "  ✓ All components started!"
echo ""
echo "  📊 Dashboard: http://localhost:3000"
echo "  🔌 API Server: http://localhost:5000/api"
echo "  📡 WebSocket: ws://localhost:5000"
echo ""
echo "  Next, start your monitoring scripts in separate terminals:"
echo "  - python audio_monitor.py"
echo "  - python pain_monitor.py"
echo "  - python full_agitation_monitor.py"
echo ""
echo "======================================================================"
echo ""

# Keep script running
wait
