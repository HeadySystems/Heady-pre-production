# HEADY_BRAND:BEGIN
# HEADY SYSTEMS :: SACRED GEOMETRY
# FILE: backend/python_worker/heady_project/utils.py
# LAYER: backend
# 
#         _   _  _____    _    ____   __   __
#        | | | || ____|  / \  |  _ \ \ \ / /
#        | |_| ||  _|   / _ \ | | | | \ V / 
#        |  _  || |___ / ___ \| |_| |  | |  
#        |_| |_||_____/_/   \_\____/   |_|  
# 
#    Sacred Geometry :: Organic Systems :: Breathing Interfaces
# HEADY_BRAND:END

import logging
import os
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def get_logger(name: str) -> logging.Logger:
    """Returns a configured logger."""
    return logging.getLogger(name)

def get_version(override: Optional[str] = None) -> str:
    """
    Returns the project version.
    Prioritizes argument override, then environment variable, then defaults to v12.3.
    """
    if override:
        return override
    return os.getenv("HEADY_VERSION", "v12.3")
