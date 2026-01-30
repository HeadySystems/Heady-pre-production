# Script to securely copy the Heady API Key to the clipboard
# Usage: ./scripts/copy_heady_key.ps1

$EnvFile = ".env"
if (-not (Test-Path $EnvFile)) {
    Write-Host "Error: .env file not found in current directory." -ForegroundColor Red
    exit 1
}

# Extract the key using regex to avoid loading all vars
$Key = Get-Content $EnvFile | Select-String "^HEADY_API_KEY=(.+)$" | ForEach-Object { $_.Matches.Groups[1].Value.Trim() }

if (-not $Key) {
    Write-Host "Error: HEADY_API_KEY not found in .env file." -ForegroundColor Red
    exit 1
}

# Copy to clipboard
$Key | Set-Clipboard

Write-Host "✅ HEADY_API_KEY has been copied to your clipboard." -ForegroundColor Green
Write-Host "   You can now paste it into your SSH session or configuration." -ForegroundColor Gray
