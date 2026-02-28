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
import typer, subprocess, sys

import labware.console as output

from pathlib import Path

from . labware import config, errorExit, outlog, log as logger, registry


app = typer.Typer(name="install", rich_markup_mode="rich", no_args_is_help=True)


#-------------------------------------------------------------------
# MODULE VARIABLES
#-------------------------------------------------------------------
NEW_USER: str
SCR_PATH: Path = Path(__file__).resolve()

#-------------------------------------------------------------------
# MODULE COMMANDS
#-------------------------------------------------------------------
def cmd(debug: Optional[bool] = False) -> None:
    """ Installer Entrypoint """
    try:
        if not checkPython():
            errorExit("Python version 3.10 or higher required", 1)
        if debug:
            output.printDebug(f"Script Path: {SCR_PATH}")
            logger.debug(f"Installing Labware")
        output.rule("[bold yellow]Installing Labware")
        output.line()

    except:
        pass

#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def checkPython() -> bool:
    """ Check if using a compatible version """
    if sys.version_info >= (3, 10):
        return False
    return True

def run(command: str, check=True, capture=False, input_txt=None):
    """ Execute shell command with error handling """
    try:
        if not capture:
            printDot(f"{command}")
        result = subprocess.run(command, shell=True, check=check, text=True, capture_output=capture, input=input_txt)
        return result
    except subprocess.CalledProcessError as e:
        outlog.logError(f"Command failed: {command}\n{e.stderr.strip()}")
        if check:
            sys.exit(1)
        return e

def getSudoUsers():
    """ Get list of users in sudo group """
    result = run("getent group sudo | cut -d: -f4", capture=True)
    return result.stdout.strip().split(',') if result.stdout.strip() else []

def promptUsername():
    """ Smart Username Prompt """
    global NEW_USER
    existing_users = getSudoUsers()
    if existing_users and existing_users != ['']:
        printSuccess(f"Found existing sudo users: {', '.join(existing_users)}")
        use_existing = input("Use an existing sudo user? (y/N): ").lower()
        if use_existing == 'y':
            while True:
                user = input("Enter existing username: ").strip().lower()
                if user in existing_users:
                    NEW_USER = user
                    printSuccess(f"Using existing sudo user: {NEW_USER}")
                    return
                printError(f"User '{user}' not found or not in sudo group.")
        while True:
            user = input("New sudo username: ").strip().lower()
            if user.isalnum() and len(user) <= 32:
                NEW_USER = user
                break
            printError(f"Use lowercase alphanumeric, max 32 chars")
