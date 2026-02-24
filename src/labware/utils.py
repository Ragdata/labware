#!/usr/bin/env python3
"""
====================================================================
Package: labware
====================================================================
Author:			Ragdata
Date:			20/02/2026
License:		MIT License
Repository:		https://github.com/Ragdata/labware
Copyright:		Copyright © 2026 Redeyed Technologies
====================================================================
"""
import shutil

from pathlib import Path
from datetime import datetime


#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def backupFile(filepath: Path, backupdir: Path = "./") -> bool:
    """Backup a file to the specified directory"""
    if not filepath.exists():
        raise FileNotFoundError(f"{filepath} does not exist")
    if not backupdir.exists():
        backupdir.mkdir(parents=True, exist_ok=True, mode=0o755)

    now = datetime.now()

    backupfile = backupdir / f"{filepath.name}.bak.{now.timestamp()}"

    try:
        shutil.copy2(filepath, backupfile)
    except Exception as e:
        raise RuntimeError(f"Failed to backup file '{filepath}': {e}'")
    return True

