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

from rich.text import Text
from rich.theme import Theme
from rich.measure import Measurement
from rich.console import Console, ConsoleOptions, RenderableType

from typing import Optional, Union

from .. labware import config

_theme = Theme({
    "info": config.get("styles", "info"),
    "success": config.get("styles", "success"),
    "warning": config.get("styles", "warning"),
    "error": config.get("styles", "error"),
    "tip": config.get("styles", "tip"),
    "important": config.get("styles", "important"),
    "debug": config.get("styles", "debug"),
    "head": config.get("styles", "head"),
    "dot": config.get("styles", "dot"),
})

console = Console(theme=_theme)

def clear(home=True) -> None:
    """
    Clear the console.

    Args:
    	home (bool): If True, clear the console and move the cursor to the home position.
    """
    console.clear(home)

def getData(prompt: Union[str, Text], **kwargs) -> str:
    """
    Get user input from the console.

    Args:
    	prompt (Union[str, Text]): The prompt to display to the user.
    	**kwargs: Arbitrary keyword arguments.

    Returns:
    	str: The user input.
    """
    return console.input(prompt, **kwargs)

def line(count=1) -> None:
    """
    Add a newline in the console.

    Args:
    	count (int): The number of newlines to add (default: 1).
    """
    console.line(count)

def measure(renderable: RenderableType, options: Optional[ConsoleOptions] = None) -> Measurement:
    """
	Measure the size of a renderable object.

	Args:
		renderable (RenderableType): The object to measure.
		options (Optional[ConsoleOptions]): Console options for measurement.

	Returns:
		Measurement: The measured size of the renderable.
	"""
    return console.measure(renderable, options=options)

def pager(renderable: RenderableType, **kwargs) -> None:
    """
	Display a renderable object in a pager.

	Args:
		renderable (RenderableType): The object to display.
		**kwargs: Arbitrary keyword arguments.
	"""
    with console.pager(**kwargs):
        console.print(renderable)

def printHeader(style: Optional[str] = None, banner: Optional[Path] = None, **kwargs) -> None:
    """
	Print the dotfiles banner and copyright information.
	"""
    msg = ""
    if banner.exists():
        with open(banner, 'r') as f:
            for lne in f:
                msg += lne
    if msg:
        console.print(msg, style=style, highlight=False, **kwargs)

def printMessage(msg: str, style: Optional[str] = None, **kwargs) -> None:
    """
	Print a message with an optional style.

	Args:
		msg (str): 	    The message to print.
		style (str):    The style to apply to the message. (Optional)
		**kwargs: 	    Arbitrary keyword arguments. (Optional)
	"""
    if style:
        console.print(msg, style=style, highlight=False, **kwargs)
    else:
        console.print(msg, highlight=False, **kwargs)

def printInfo(msg: str, **kwargs) -> None:
    """
    Print an INFO message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "info")
    msg = f"{symbol} " + msg
    printMessage(msg, style="info", **kwargs)

def printSuccess(msg: str, **kwargs) -> None:
    """
    Print a SUCCESS message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "success")
    msg = f"{symbol} " + msg
    printMessage(msg, style="success", **kwargs)

def printWarning(msg: str, **kwargs) -> None:
    """
    Print a WARNING message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "warning")
    msg = f"{symbol} " + msg
    printMessage(msg, style="warning", **kwargs)

def printError(msg: str, **kwargs) -> None:
    """
    Print an ERROR message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "error")
    msg = f"{symbol} " + msg
    printMessage(msg, style="error", **kwargs)

def printTip(msg: str, **kwargs) -> None:
    """
    Print a TIP message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "tip")
    msg = f"{symbol} " + msg
    printMessage(msg, style="tip", **kwargs)

def printImportant(msg: str, **kwargs) -> None:
    """
    Print an IMPORTANT message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "important")
    msg = f"{symbol} " + msg
    printMessage(msg, style="important", **kwargs)

def printDebug(msg: str, **kwargs) -> None:
    """
    Print a DEBUG message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "debug")
    msg = f"{symbol} " + msg
    printMessage(msg, style="debug", **kwargs)

def printHead(msg: str, **kwargs) -> None:
    """
    Print a HEAD message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "head")
    msg = f"{symbol} " + msg
    printMessage(msg, style="head", **kwargs)

def printDot(msg: str, **kwargs) -> None:
    """
    Print a DOT message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "dot")
    msg = f"{symbol} " + msg
    printMessage(msg, style="dot", **kwargs)

def printRed(msg: str, **kwargs) -> None:
    """
    Print a message in RED

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        printMessage(msg, style="bright_red", **kwargs)
    else:
        printMessage(msg, style="red", **kwargs)

def printGreen(msg: str, **kwargs) -> None:
    """
    Print a message in GREEN

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        printMessage(msg, style="bright_green", **kwargs)
    else:
        printMessage(msg, style="green", **kwargs)

def printBlue(msg: str, **kwargs) -> None:
    """
    Print a message in BLUE

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        printMessage(msg, style="bright_blue", **kwargs)
    else:
        printMessage(msg, style="blue", **kwargs)

def printYellow(msg: str, **kwargs) -> None:
    """
    Print a message in YELLOW

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        printMessage(msg, style="bright_yellow", **kwargs)
    else:
        printMessage(msg, style="yellow", **kwargs)

def printPurple(msg: str, **kwargs) -> None:
    """
    Print a message in PURPLE

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        printMessage(msg, style="bright_magenta", **kwargs)
    else:
        printMessage(msg, style="magenta", **kwargs)

def printCyan(msg: str, **kwargs) -> None:
    """
    Print a message in CYAN

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        printMessage(msg, style="bright_cyan", **kwargs)
    else:
        printMessage(msg, style="cyan", **kwargs)

def printWhite(msg: str, **kwargs) -> None:
    """
    Print a message in WHITE

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        printMessage(msg, style="bright_white", **kwargs)
    else:
        printMessage(msg, style="white", **kwargs)

def rule(*args) -> None:
    """
	Draw a line with optional title
	"""
    console.rule(*args)

def status(arg: Union[str, Text], **kwargs) -> None:
    """
	Display a status and spinner
	"""
    console.status(arg, **kwargs)


#-------------------------------------------------------------------
# OutLog Class
#-------------------------------------------------------------------
class Outlog(object):
    """
    A class to handle console message with concurrent logging
    """

    _logger = None

    def __init__(self, logger):
        """
        Initialize the OutLog instance.

        Args:
        	logger: An optional logger instance for logging messages.
        """
        self._logger = logger

    def logMessage(self, msg: str, level: int = config.get("logging", "level"), style: Optional[str] = None, **kwargs) -> None:
        """
        Log and print a message with an optional style.

        Args:
        	msg (str):      The message to log and print.
        	level (int):    The level of the message to log and print.
        	style (str):    The style to apply to the message. (Optional)
        	**kwargs:       Arbitrary keyword arguments.
        """
        if self._logger.isEnabledFor(level):
            self._logger.log(level, msg)
        symbol = None
        match style:
            case "debug":
                symbol = config.get("symbols", "debug")
            case "info":
                symbol = config.get("symbols", "info")
            case "warning":
                symbol = config.get("symbols", "warning")
            case "error":
                symbol = config.get("symbols", "error")
        if symbol is not None:
            msg = f"{symbol} " + msg
        printMessage(msg, style=style, **kwargs)

    def logDebug(self, msg: str, **kwargs) -> None:
        """
        Log a DEBUG message.

        Args:
        	msg (str): The message to log.
        	**kwargs: Arbitrary keyword arguments.
        """
        self.logMessage(msg, level=logging.DEBUG, style="debug", **kwargs)

    def logInfo(self, msg: str, **kwargs) -> None:
        """
        Log an INFO message.

        Args:
        	msg (str): The message to log.
        	**kwargs: Arbitrary keyword arguments.
        """
        self.logMessage(msg, level=logging.INFO, style="info", **kwargs)

    def logWarning(self, msg: str, **kwargs) -> None:
        """
        Log a WARNING message.

        Args:
        	msg (str): The message to log.
        	**kwargs: Arbitrary keyword arguments.
        """
        self.logMessage(msg, level=logging.WARNING, style="warning", **kwargs)

    def logError(self, msg: str, **kwargs) -> None:
        """
        Log an ERROR message.

        Args:
        	msg (str): The message to log.
        	**kwargs: Arbitrary keyword arguments.
        """
        self.logMessage(msg, level=logging.ERROR, style="error", **kwargs)

    def logSuccess(self, msg: str, **kwargs) -> None:
        """
        Log a SUCCESS message.

        Args:
        	msg (str): The message to log.
        	**kwargs: Arbitrary keyword arguments.
        """
        self.logMessage(msg, level=logging.INFO, style="success", **kwargs)

    def logCritical(self, msg: str, **kwargs) -> None:
        """
        Log an ERROR message.

        Args:
        	msg (str): The message to log.
        	**kwargs: Arbitrary keyword arguments.
        """
        self.logMessage(msg, level=logging.CRITICAL, style="error", **kwargs)

    def logFatal(self, msg: str, **kwargs) -> None:
        """
        Log an ERROR message.

        Args:
        	msg (str): The message to log.
        	**kwargs: Arbitrary keyword arguments.
        """
        self.logMessage(msg, level=logging.FATAL, style="error", **kwargs)


