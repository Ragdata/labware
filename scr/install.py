#!/usr/bin/env python3
"""
====================================================================
Package: labware
====================================================================
Author:			Ragdata
Date:			01/03/2026
License:		MIT License
Repository:		https://github.com/Ragdata/labware
Copyright:		Copyright © 2026 Redeyed Technologies
====================================================================
"""
import subprocess, pip, sys, os

from pathlib import Path

from . console import *
from . labware import config, errorExit, outlog, log as logger, registry

#-------------------------------------------------------------------
# SCRIPT VARIABLES
#-------------------------------------------------------------------
NEW_USER: str
SCR_PATH: Path = Path(__file__).resolve()


#-------------------------------------------------------------------
# SCRIPT FUNCTIONS
#-------------------------------------------------------------------
def checkPython() -> bool:
    if sys.version_info < (3, 12):
        return False
    return True

def checkUser() -> bool:
    euid = os.geteuid()
    if euid != 0:
        return False
    return True


#-------------------------------------------------------------------
# SCRIPT
#-------------------------------------------------------------------
def run():
    if not checkUser():
        raise RuntimeError("This package needs to be run as root or with sudo privileges")
    if not checkPython():
        raise RuntimeError("This package requires python version 3.12 or greater")
    pipver = pip.__version__
    piparr = pipver.split('.')
    if piparr[0] < 26:
        raise RuntimeError("This package reqires pip version 26.0.0 or greater")

if __name__ == '__main__':
    run()
