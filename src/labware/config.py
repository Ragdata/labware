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
import logging

from pathlib import Path

SYMBOL_ERROR = "✘"
SYMBOL_WARNING = "🛆"
SYMBOL_INFO = "✚"
SYMBOL_SUCCESS = "🗸"
SYMBOL_TIP = "★"
SYMBOL_IMPORTANT = "⚑"
SYMBOL_DEBUG = "⚙"
SYMBOL_HEAD="➤"
SYMBOL_DOT="⦁"

STYLE_ERROR = "bold red"
STYLE_WARNING = "bold yellow"
STYLE_INFO = "bright_blue"
STYLE_SUCCESS = "bright_green"
STYLE_TIP = "cyan"
STYLE_IMPORTANT = "magenta"
STYLE_DEBUG = "dim white"
STYLE_HEAD = "bold yellow"
STYLE_DOT = "green"

LOG_DIR = "/var/log/labware"
LOG_LEVEL = logging.INFO
LOG_SIZE = 1 * 1024 * 1024 # 1MB
LOG_COUNT = 3

STD_FORMAT = "%(asctime)s :: %(levelname)s :: %(message)s"
SHORT_FORMAT = "%(levelname)s :: %(message)s"
LONG_FORMAT = "%(asctime)s :: %(levelname)s :: %(message)s in %(filename)s\n%(pathname)s [ %(funcName)s line %(lineno)s ]"
CON_FORMAT = "%(message)s"
