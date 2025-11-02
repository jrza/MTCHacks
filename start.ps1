# CineDeen Simple Start Script (Windows)
# This version uses simpler process management

Write-Host "🎬 Starting CineDeen..." -ForegroundColor Green
Write-Host ""

# Get local IP
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -notlike "169.254.*" } | Select-Object -First 1).IPAddress
if (-not $localIP) { $localIP = "127.0.0.1" }

Write-Host "📡 Local IP: $localIP" -ForegroundColor Cyan

# Check port 8000
$portInUse = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($portInUse) {
    Write-Host "⚠️  Killing process on port 8000..." -ForegroundColor Yellow
    $pid = ($portInUse | Select-Object -First 1).OwningProcess
    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Host "🚀 Starting Backend (new window)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; Write-Host '🎬 CineDeen Backend' -ForegroundColor Green; py main.py"

Write-Host "   Waiting for backend..."
Start-Sleep -Seconds 5

# Check backend
$backendOk = $false
for ($i = 1; $i -le 10; $i++) {
    try {
        $null = Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        Write-Host "   ✅ Backend ready!" -ForegroundColor Green
        $backendOk = $true
        break
    } catch {
        Start-Sleep -Seconds 1
    }
}

if (-not $backendOk) {
    Write-Host "   ⚠️  Backend may need more time..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📱 Starting Frontend (new window)..." -ForegroundColor Yellow
Write-Host "   Backend URL: http://$localIP:8000" -ForegroundColor Cyan

# Set environment and start frontend
$env:EXPO_PUBLIC_API_URL = "http://$localIP:8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:EXPO_PUBLIC_API_URL='http://$localIP:8000'; cd '$PSScriptRoot\frontend'; Write-Host '📱 CineDeen Frontend' -ForegroundColor Green; Write-Host 'Backend URL: http://$localIP:8000' -ForegroundColor Cyan; npm start"

Write-Host ""
Write-Host "✨ CineDeen is starting!" -ForegroundColor Green
Write-Host ""
Write-Host "   Backend:  http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "   Frontend: Opens in new window (scan QR with Expo Go)" -ForegroundColor Cyan
Write-Host ""
Write-Host "To stop: Close the backend and frontend windows" -ForegroundColor Yellow
Write-Host ""

