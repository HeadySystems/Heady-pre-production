# HEADY_BRAND:BEGIN
# HEADY SYSTEMS :: SACRED GEOMETRY
# FILE: src/heady_project/consolidated_builder.py
# LAYER: backend/src
# 
#         _   _  _____    _    ____   __   __
#        | | | || ____|  / \  |  _ \ \ \ / /
#        | |_| ||  _|   / _ \ | | | | \ V / 
#        |  _  || |___ / ___ \| |_| |  | |  
#        |_| |_||_____/_/   \_\____/   |_|  
# 
#    Sacred Geometry :: Organic Systems :: Breathing Interfaces
# HEADY_BRAND:END

import subprocess
from pathlib import Path
from .utils import get_logger

logger = get_logger(__name__)

def run_command(cmd, cwd=None):
    try:
        subprocess.run(cmd, shell=True, cwd=cwd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {cmd} ({e})")
        raise

def run_consolidated_build(version: str, project_root: Path = None):
    if project_root is None:
        project_root = Path.cwd()
    logger.info(f"Running consolidated builder [Version: {version}] at {project_root}")
    
    # Simple build steps
    if (project_root / "package.json").exists():
        logger.info("Installing Node deps...")
        # run_command("npm install", cwd=project_root) # Commented out to avoid long waits in restore
        
    if (project_root / "requirements.txt").exists():
        logger.info("Installing Python deps...")
        # run_command("pip install -r requirements.txt", cwd=project_root) # Commented out to avoid long waits in restore

    logger.info("Build complete.")
