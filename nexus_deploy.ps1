# HEADY NEXUS DEPLOYMENT PROTOCOL
# Executed via Windsurf Terminal

$ROOT = $PSScriptRoot
Set-Location $ROOT

Write-Host "∞ INITIATING WINDSURF NEXUS EVENT ∞" -ForegroundColor Cyan

# 1. PRE-PUSH OPTIMIZATION
Write-Host "`n[1/4] Optimizing Monorepo Structure..." -ForegroundColor Yellow
if (Test-Path "backend/index.js") {
    Write-Host "✓ Optimized structure detected." -ForegroundColor Green
} else {
    Write-Host "! Structure optimization required. Run local build first." -ForegroundColor Red
    exit 1
}

# 2. GIT SYNC
Write-Host "`n[2/4] Syncing Changes..." -ForegroundColor Yellow
git add .
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
try {
    git commit -m "Nexus Sync: $timestamp [Optimized Monorepo]" -ErrorAction SilentlyContinue
} catch {}

# 3. CONFIGURE REMOTES (The 5 Pillars)
Write-Host "`n[3/4] Aligning Remotes..." -ForegroundColor Yellow
function Add-Remote ($name, $url) {
    if (git remote get-url $name 2>$null) {
        git remote set-url $name $url
    } else {
        git remote add $name $url
    }
}

# Core Remotes - Correcting common naming/path issues
Add-Remote "heady-me"   "git@github.com:HeadyMe/Heady.git"
Add-Remote "heady-sys"  "git@github.com:HeadySystems/Heady.git"
Add-Remote "sandbox"    "git@github.com:HeadySystems/sandbox.git"
Add-Remote "origin"     "git@github.com:HeadySystems/Heady.git" # Set origin to the system-primary

Write-Host "✓ Remotes aligned." -ForegroundColor Green

# 4. DISTRIBUTION PROTOCOL
Write-Host "`n[4/4] Distributing to Nexus..." -ForegroundColor Yellow
function Push-To-Remote ($remoteName) {
    Write-Host "Pushing to $remoteName..." -NoNewline
    # Use -u for the primary origin, otherwise just push
    if ($remoteName -eq "origin") {
        $output = git push -u $remoteName main --force 2>&1
    } else {
        $output = git push $remoteName main --force 2>&1
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host " [SUCCESS]" -ForegroundColor Green
    } else {
        Write-Host " [FAILED]" -ForegroundColor Red
        Write-Host "  $output" -ForegroundColor DarkGray
    }
}

$remotes = "origin", "heady-me", "heady-sys", "sandbox"
foreach ($r in $remotes) {
    Push-To-Remote $r
}

Write-Host "`n∞ NEXUS EVENT COMPLETE ∞" -ForegroundColor Cyan
