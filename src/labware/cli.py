#!/usr/bin/env python3
"""
====================================================================
Package: labware
====================================================================
Author:			Ragdata
Date:			26/02/2026
License:		MIT License
Repository:		https://github.com/Ragdata/labware
Copyright:		Copyright © 2026 Redeyed Technologies
====================================================================
"""
import typer, rich, os

import labware.install as installer

from typing import Union
from enum import Enum
from typing_extensions import Annotated

from . console import *

from labware import config, log as logger, outlog, registry
from labware import __pkg_name__, __version__


#-------------------------------------------------------------------
# Initialization
#-------------------------------------------------------------------
app = typer.Typer(name="labware", rich_markup_mode="rich", invoke_without_command=True)

app.add_typer(installer.app, name="install", help="Installer", rich_help_panel="Labware Subcommands")


@app.callback()
def callback() -> None:
    pass

#-------------------------------------------------------------------
# CLI Functions
#-------------------------------------------------------------------
@app.command()
def env() -> None:
    """ Print current environment variables. """
    printInfo("Current Environment Variables:")
    for key, value in os.environ.items():
        printMessage(f"{key}: {value}")

@app.command()
def install(debug: Annotated[bool, typer.Option("--debug", "-d", help="", rich_help_panel="Output Panel")] = False) -> None:
    """ Install the package and its dependencies. """
    installer.cmd(debug=debug)

@app.command()
def uninstall():
    pass

@app.command()
def version(
    silent: Annotated[bool, typer.Option("--silent", "-s", help="Return version as variable", rich_help_panel="Output Panel")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Print package name & version", rich_help_panel="Output Panel")] = False,
    vverbose: Annotated[bool, typer.Option("--very-verbose", "-vv", help="Print version data with copyright information", rich_help_panel="Output Panel")] = False
) -> Union[str, None]:
    """ Print the package version information. """
    if silent:
        return __version__
    elif verbose:
        printMessage(f"{__pkg_name__.capitalize()} v{__version__}")
    elif vverbose:
        printMessage(f"{__pkg_name__.capitalize()} v{__version__} ~ Copyright © 2026 Redeyed Technologies", style="yellow")
    else:
        printMessage(f"{__version__}")
    return None


if __name__ == "__main__":
    app()
