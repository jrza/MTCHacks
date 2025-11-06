hello mohammed

# CineDeen - Islamic Media Recommender

Unified fullstack app for recommending movies with Islamic-lens analysis.

## 🚀 Quick Start (One Command)

### Install Dependencies (First Time Only)

```bash
npm run install:all
```

This installs:
- Backend: FastAPI, Uvicorn, python-dotenv
- Frontend: Expo SDK 54, React Native, Axios

### Start Everything

**Windows:**
```bash
npm start
```
Or directly: `.\start-simple.ps1`

**Linux/Mac:**
```bash
npm run start:unix
```
Or directly: `bash start.sh`

The script will:
1. ✅ Auto-detect your local IP address
2. ✅ Start backend on http://127.0.0.1:8000
3. ✅ Start frontend Expo server
4. ✅ Configure frontend to connect to backend automatically

## 📱 Using the App

1. **Start the app** with `npm start`
2. **Open Expo Go** on your phone
3. **Scan the QR code** that appears in terminal
4. Make sure your phone and computer are on the **same WiFi network**

## 🔧 Manual Start (If Needed)

### Backend Only
```bash
cd backend
py main.py  # Windows
python main.py  # Linux/Mac
```

### Frontend Only
```bash
cd frontend
npm start
```

## 📡 Network Configuration

The start script automatically:
- Detects your local IP address
- Configures frontend to connect to backend
- Works with Expo Go tunnel mode

**For physical devices:** The app will use your computer's local IP (e.g., `http://192.168.1.100:8000`)

**For emulators:**
- Android Emulator: `http://10.0.2.2:8000`
- iOS Simulator: `http://localhost:8000`

## 🏗️ Project Structure

```
MTCHacks/
├── backend/              # FastAPI backend
│   ├── main.py          # Run with: py main.py
│   └── ...
├── frontend/            # React Native Expo app (SDK 54)
│   ├── App.js           # Auto-detects backend URL
│   └── ...
├── start.ps1            # Windows start script
├── start.sh             # Linux/Mac start script
├── start.js             # Cross-platform orchestrator
└── package.json         # Root npm scripts
```

## ✨ Features

- **One Command Setup**: `npm start` runs everything
- **Auto-Detection**: Automatically finds backend URL
- **Cross-Platform**: Works on Windows, Linux, Mac
- **Fully Local**: No external APIs needed
- **Single Profile**: Simple, no authentication

## 📋 API Endpoints

- `GET /recommend` - Get current movie recommendations
- `POST /refresh` - Refresh recommendations
- `GET /health` - Health check

## 🐛 Troubleshooting

**Port 8000 already in use:**
```bash
# Find and kill process
netstat -ano | findstr :8000  # Windows
lsof -ti:8000 | xargs kill    # Linux/Mac
```

**Frontend can't connect to backend:**
- Make sure backend is running (`http://127.0.0.1:8000/health`)
- Check firewall settings
- Ensure phone and computer are on same WiFi
