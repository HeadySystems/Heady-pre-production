param([string]$Mode, [string]$Subject)
$BASE = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
python "$BASE\Tools\Content_Generator.py" $Mode $Subject
