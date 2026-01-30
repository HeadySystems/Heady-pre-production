# Scripts/colab_bridge.ps1
# Exposes the local repository to Google Colab via Ngrok
# Usage: .\scripts\colab_bridge.ps1

Write-Host "🌉 Starting Colab Bridge..." -ForegroundColor Cyan

# 1. Check Prerequisites
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: Python is required to run the local file server." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command "ngrok" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: Ngrok CLI is required. Please install it first." -ForegroundColor Red
    Write-Host "   choco install ngrok" -ForegroundColor Gray
    exit 1
}

# 2. Ngrok Auth
$AuthToken = $env:NGROK_AUTHTOKEN
if (-not $AuthToken) {
    Write-Host "⚠️  NGROK_AUTHTOKEN not found in environment." -ForegroundColor Yellow
    $AuthToken = Read-Host "Please enter your Ngrok Authtoken"
    if ($AuthToken) {
        ngrok config add-authtoken $AuthToken
    } else {
        Write-Host "❌ Authtoken is required." -ForegroundColor Red
        exit 1
    }
}

# 3. Start Local File Server
$Port = 8081
Write-Host "📂 Starting Local File Server on port $Port..." -ForegroundColor Cyan
$ServerJob = Start-Job -ScriptBlock {
    param($p)
    python -m http.server $p
} -ArgumentList $Port

Start-Sleep -Seconds 2

# 4. Start Ngrok Tunnel
Write-Host "🚀 Starting Ngrok Tunnel..." -ForegroundColor Cyan
# Using Start-Process to run in separate window or background
# We'll use Start-Job for this demo flow, but ngrok needs to stay alive
# Ideally, we run ngrok and parse the output
$NgrokProcess = Start-Process -FilePath "ngrok" -ArgumentList "http $Port" -PassThru -NoNewWindow

Write-Host "`n✅ Bridge Established!" -ForegroundColor Green
Write-Host "---------------------------------------------------------"
Write-Host "1. Go to your Ngrok Dashboard: https://dashboard.ngrok.com/endpoints"
Write-Host "2. Copy the public URL (e.g. https://xxxx.ngrok-free.app)"
Write-Host "3. In Colab, run:"
Write-Host "   !git clone https://xxxx.ngrok-free.app/ local_repo"
Write-Host "   (Note: http.server exposes files, git clone needs a git server."
Write-Host "    If you just need files, use !wget -r ...)"
Write-Host "---------------------------------------------------------"
Write-Host "Press any key to stop the bridge..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Stop-Job $ServerJob
Stop-Process -Id $NgrokProcess.Id -Force
Write-Host "🛑 Bridge Stopped." -ForegroundColor Red
