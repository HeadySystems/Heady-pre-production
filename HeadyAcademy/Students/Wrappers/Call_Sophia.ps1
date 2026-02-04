param([string]$Tool)
$BASE = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Write-Host "[SOPHIA] Learning tool $Tool..."
python "$BASE\Tools\Tool_Learner.py" $Tool
