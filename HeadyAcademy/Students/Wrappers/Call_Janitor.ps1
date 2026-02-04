param([string]$Target)
$BASE = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Write-Host "[JANITOR] Cleaning $Target..."
python "$BASE\Tools\Clean_Sweep.py" $Target
