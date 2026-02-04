param([string]$Target)
$BASE = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Write-Host "[MURPHY] Running security audit on $Target..."
python "$BASE\Tools\Security_Audit.py" $Target
