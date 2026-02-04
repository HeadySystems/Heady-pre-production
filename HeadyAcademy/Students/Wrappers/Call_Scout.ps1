param([string]$Query)
$BASE = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Write-Host "[SCOUT] Scanning GitHub for $Query..."
python "$BASE\Tools\Github_Scanner.py" $Query
