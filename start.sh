#!/bin/bash
# CineDeen Unified Start Script (Linux/Mac)

echo "🎬 Starting CineDeen Fullstack App..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.9+ and try again."
    exit 1
fi

PYTHON_CMD=$(command -v python3 || command -v python)

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please install Node.js and try again."
    exit 1
fi

# Get local IP address
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "127.0.0.1")
else
    # Linux
    LOCAL_IP=$(hostname -I | awk '{print $1}' 2>/dev/null || echo "127.0.0.1")
fi

echo "📡 Detected local IP: $LOCAL_IP"
echo ""

# Set environment variables for frontend
export EXPO_PUBLIC_API_URL="http://$LOCAL_IP:8000"
export REACT_NATIVE_PACKAGER_HOSTNAME=$LOCAL_IP

# Check if port 8000 is already in use
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 8000 is already in use. Stopping existing process..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    sleep 2
fi

echo "🚀 Starting Backend..."
cd backend
$PYTHON_CMD main.py &
BACKEND_PID=$!
cd ..

sleep 3

# Check if backend started successfully
if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running on http://127.0.0.1:8000"
else
    echo "⚠️  Backend may still be starting..."
fi

echo ""
echo "📱 Starting Frontend..."
echo "   Backend URL: http://$LOCAL_IP:8000"
echo ""

cd frontend
npm start &
FRONTEND_PID=$!

echo ""
echo "✨ CineDeen is starting!"
echo "   Backend: http://127.0.0.1:8000"
echo "   Frontend: Expo will open in a new window"
echo ""
echo "Press CTRL+C to stop both services"

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait

