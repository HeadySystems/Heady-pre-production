param([string]$Repo)
$BASE = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Write-Host "[OCULUS] Visualizing $Repo..."
python "$BASE\Tools\Visualizer.py" $Repo
