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
import typer, subprocess, shutil, sys, os

from pathlib import Path
from typing import Optional

from src.labware import config, log as logger, outlog, errorExit

from . console import *

app = typer.Typer(name="install", rich_markup_mode="rich", no_args_is_help=True)


#-------------------------------------------------------------------
# MODULE VARIABLES
#-------------------------------------------------------------------
NEW_USER: str
SCR_PATH: Path = Path(__file__).resolve()
REPO_PATH: Path = SCR_PATH.parent.parent

#-------------------------------------------------------------------
# MODULE COMMANDS
#-------------------------------------------------------------------
def cmd(debug: Optional[bool] = False) -> None:
    """ Installer Entrypoint """
    if not checkPython():
        errorExit("Python version 3.12 or higher required", 1)
    if not checkUser():
        errorExit("This package MUST be run as root or with sudo privileges", 1)
    try:
        if debug:
            printDebug(f"Module Path: {SCR_PATH}")
            printDebug(f"Repo Path: {REPO_PATH}")
        logger.info("Installing Labware")
        rule("[bold yellow]Installing Labware")
        line()
        copyFiles(debug)
        new_user = input("Do you want to create a new sudo user? (Y/n): ").lower()
        if new_user == "y" or not new_user:
            pass
    except:
        pass

#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def checkPython() -> bool:
    """ Check if using a compatible version """
    if sys.version_info >= (3, 12):
        return False
    else:
        return True

def checkUser() -> bool:
    if os.geteuid() != 0:
        return False
    else:
        return True

def copyFiles(debug: Optional[bool] = False) -> bool:
    try:
        for name, stub in config['dirs'].items():
            repodir = REPO_PATH / stub
            userdir = Path.home() / '.labware' / stub
            if not userdir.exists():
                os.mkdir(userdir, 0o755)
            for filename in os.scandir(repodir):
                filepath = filename.path
                userpath = userdir / filename.name
                if debug:
                    outlog.logDebug(f"Copying '{filepath}' to '{userpath}'")
                if filename.is_file():
                    shutil.copy2(filepath, userdir)
                elif filename.is_dir():
                    shutil.copytree(filepath, userpath)
    except Exception as e:
        errorExit("File Copy Error")
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
