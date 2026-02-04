# HEADY_BRAND:BEGIN
# HEADY SYSTEMS :: SACRED GEOMETRY
# FILE: HeadyAcademy/Students/Wrappers/Call_Sophia.ps1
# LAYER: root
# 
#         _   _  _____    _    ____   __   __
#        | | | || ____|  / \  |  _ \ \ \ / /
#        | |_| ||  _|   / _ \ | | | | \ V / 
#        |  _  || |___ / ___ \| |_| |  | |  
#        |_| |_||_____/_/   \_\____/   |_|  
# 
#    Sacred Geometry :: Organic Systems :: Breathing Interfaces
# HEADY_BRAND:END

param([string]$Tool)
$BASE = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Write-Host "[SOPHIA] Learning tool $Tool..."
python "$BASE\Tools\Tool_Learner.py" $Tool
