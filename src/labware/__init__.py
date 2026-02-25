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
from pathlib import Path
from configparser import ConfigParser

from .logger import Logger, getFormatter, initRotatingFileHandler

__pkg_name__ = 'labware'
__version__ = '0.1.0'

config = ConfigParser()
config.read('labware/.default.cfg')

user_dir = Path.home()
user_cfg = user_dir / '.labware.cfg'
if user_cfg.exists():
    config.read(user_cfg)

from . logger import LOG_LEVEL, LOG_SIZE, LOG_COUNT, LOG_FORMAT

#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def version(output: bool = True):
    """Print the package version"""
    if output:
        # Print version to console
		print(f"{__pkg_name__.capitalize()} version {__version__}")
    else:
        # Return the version string
		return f"{__version__}"
    return None

def getFileLogger(name: str, level: int = LOG_LEVEL, fmt: str = LOG_FORMAT) -> Logger:
    """ Retrieve or create a logger instance """
    formatter = getFormatter(fmt)
    handler = initRotatingFileHandler(name, level=level, maxSize=LOG_SIZE, backups=LOG_COUNT)
    handler.setFormatter(formatter)
    log = Logger(name, level=level)
    log.addHandler(handler)
    return log
