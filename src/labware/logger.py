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
import sys, logging

from pathlib import Path
from typing import TextIO, Any
from logging.handlers import RotatingFileHandler

from . labware import config

LOG_LEVEL = config.getint("logging", "level")
LOG_DIR = Path(config.get("logging", "logdir"))
LOG_SIZE = config.getint("logging", "size")
LOG_COUNT = config.getint("logging", "count")
LOG_FORMAT = config.get("logging", "format")
CON_FORMAT = config.get("log_formats", "console")
DATE_FORMAT = config.get("log_formats", "date")


#-------------------------------------------------------------------
# Logger Class
#-------------------------------------------------------------------
class Logger(logging.Logger):
    """Custom labware logger class"""

    def __init__(self, name: str, level: int = LOG_LEVEL, **kwargs) -> None:
        """
        Initialize the logger with a name and level

        Args:
            name (str):     Name of the logger
            level (int):    Logging level. (Defaults to logging.INFO)
            **kwargs:       Additional keyword arguments for logging config
        """
        super().__init__(name, level)
        self.setLevel(level)

    def critical(self, msg:str, *args, **kwargs) -> None:
        """
        Log a CRITICAL message

        Args:
            msg (str):      The message to log
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.CRITICAL, msg, args, **kwargs)

    def debug(self, msg:str, *args, **kwargs) -> None:
        """
        Log a DEBUG message

        Args:
            msg (str):      The message to log
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.DEBUG, msg, args, **kwargs)

    def error(self, msg:str, *args, **kwargs) -> None:
        """
        Log an ERROR message

        Args:
            msg (str):      The message to log
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.ERROR, msg, args, **kwargs)

    def exception(self, msg:str, *args, **kwargs) -> None:
        """
        Log an ERROR message

        Args:
            msg (str):      The message to log
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.ERROR, msg, args, exc_info=True, **kwargs)

    def fatal(self, msg:str, *args, **kwargs) -> None:
        """
        Log a FATAL message

        Args:
            msg (str):      The message to log
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.FATAL, msg, args, **kwargs)

    def info(self, msg:str, *args, **kwargs) -> None:
        """
        Log an INFO message

        Args:
            msg (str):      The message to log
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.INFO, msg, args, **kwargs)

    def warning(self, msg:str, *args, **kwargs) -> None:
        """
        Log a WARNING message

        Args:
            msg (str):      The message to log
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.WARNING, msg, args, **kwargs)

    def log(self, level: int, msg: str, *args, **kwargs) -> None:
        """
        Write a message to the log with a specified level

        Args:
            level (int):    The logging level
            msg (str):      The message to log
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        if self.isEnabledFor(level):
            self._log(level, msg, args, **kwargs)


#-------------------------------------------------------------------
# initRotatingFileHandler
#-------------------------------------------------------------------
def initRotatingFileHandler(name: str, level: int = LOG_LEVEL, path: Path = LOG_DIR, maxSize: int = LOG_SIZE, backups: int = LOG_COUNT) -> RotatingFileHandler:
    """
    Initialize and return a RotatingFileHandler.

    Args:
    	name (str):     Name of the logger.
    	level (int):    Logging level for the file handler (default is LOG_LEVEL_FILE).
    	path (Path):    Directory where the log file will be stored (default is DOT_LOG).
    	maxSize (int):  Maximum size of the log file before rotation (default is 5 MB).
    	backups (int):  Number of backup files to keep (default is 5).

    Returns:
    	RotatingFileHandler: Configured file handler instance.
    """
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True, mode=0o755)
    logFile = path / f"{name}.log"
    return RotatingFileHandler(logFile, maxBytes = maxSize, backupCount = backups, encoding='utf-8', delay=False)


#-------------------------------------------------------------------
# initStreamHandler
#-------------------------------------------------------------------
def initStreamHandler(stream: TextIO | Any = sys.stdout, level: int = LOG_LEVEL, style: str = CON_FORMAT) -> logging.StreamHandler:
    """
    Initialize and return a StreamHandler.

    Args:
    	stream (TextIO | Any): The stream to which the log messages will be sent (default is sys.stdout).
    	level (int): Logging level for the stream handler (default is LOG_LEVEL_STREAM).
    	style (str): Log format string (default is CON_FORMAT).

    Returns:
    	logging.StreamHandler: Configured stream handler instance.
    """
    handler = logging.StreamHandler(stream)
    handler.setLevel(level)
    return handler


#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def getFormatter(name: str = LOG_FORMAT) -> logging.Formatter:
    match name:
        case "std":
            msgFormat = config.get("log_formats", "std")
        case "short":
            msgFormat = config.get("log_formats", "short")
        case "long":
            msgFormat = config.get("log_formats", "long")
        case "console":
            msgFormat = config.get("log_formats", "console")
        case _:
            msgFormat = config.get("log_formats", "std")
    return logging.Formatter(msgFormat, datefmt=DATE_FORMAT)
