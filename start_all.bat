@echo off
REM ======================================================================
REM  Pain Watcher - Quick Start Script
REM  Run all components with one command
REM ======================================================================

echo.
echo ======================================================================
echo  🏥 ICU Pain Watcher - System Startup
echo ======================================================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install from https://nodejs.org
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install from https://www.python.org
    pause
    exit /b 1
)

echo ✓ Node.js found: 
node --version
echo.
echo ✓ Python found:
python --version
echo.

REM Create terminals for each component
echo Starting Backend...
start cmd /k "cd backend && python app.py"
timeout /t 2 >nul

echo Starting Frontend...
start cmd /k "cd frontend && npm start"
timeout /t 2 >nul

echo Starting Audio Monitor...
start cmd /k "python audio_monitor.py"
timeout /t 1 >nul

echo Starting Pain Monitor...
start cmd /k "python pain_monitor.py"
timeout /t 1 >nul

echo Starting Agitation Monitor...
start cmd /k "python full_agitation_monitor.py"
timeout /t 1 >nul

echo.
echo ======================================================================
echo  ✓ All components started!
echo.
echo  📊 Dashboard: http://localhost:3000
echo  🔌 API Server: http://localhost:5000/api
echo  📡 WebSocket: ws://localhost:5000
echo.
echo  Running Monitors:
echo  ✓ Audio Monitor (listening for keywords)
echo  ✓ Pain Monitor (watching facial expressions)
echo  ✓ Agitation Monitor (tracking body movement)
echo.
echo  Press 'q' in any monitor window to stop that monitor
echo ======================================================================
echo.

pause
