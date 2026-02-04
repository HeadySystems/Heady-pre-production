# HEADY_BRAND:BEGIN
# HEADY SYSTEMS :: SACRED GEOMETRY
# FILE: HeadyAcademy/Students/Wrappers/Call_Muse.ps1
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

param([string]$Mode, [string]$Subject)
$BASE = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
python "$BASE\Tools\Content_Generator.py" $Mode $Subject
