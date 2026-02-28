#!/usr/bin/env python3
"""
====================================================================
Package: labware
====================================================================
Author:			Ragdata
Date:			25/02/2026
License:		MIT License
Repository:		https://github.com/Ragdata/labware
Copyright:		Copyright © 2026 Redeyed Technologies
====================================================================
"""
import subprocess, sys, os, getpass, shutil, time

from pathlib import Path

from . console import *
from . labware import config, log, outlog, errorExit


#-------------------------------------------------------------------
# MODULE COMMANDS
#-------------------------------------------------------------------



#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def ckroot():
    """ Check if running as root"""
    if os.getuid() != 0:
        errorExit("This script must be run as root. Please use sudo or run as root user.")

def ckUbuntu():
    version = run("lsb_release -rs", capture=True).stdout.strip()
    if version != '24.04':
        printError(f"Expected Ubuntu 24.04, found {version}")
        if input("Continue anyway? (y/N): ").lower() != 'y':
            sys.exit(1)

def createUser():
    printHead(f"User Setup {NEW_USER}")
    if userExists():
        printWarning(f"User '{NEW_USER}' already exists. Skipping creation.")
        run(f"usermod -aG sudo {NEW_USER}", check=False)
    else:
        run(f"useradd -m -s /bin/bash -G sudo {NEW_USER}")
        printSuccess(f"User '{NEW_USER}' created and added to sudo group")
    sudoers = Path(f"/etc/sudoers.d/{NEW_USER}")
    if not sudoers.exists():
        with open(sudoers, "w") as f:
            f.write(f"{NEW_USER} ALL=(ALL) NOPASSWD:ALL\n")
            sudoers.chmod(0o644)

def getPassword():
    while True:
        pwd = getpass.getpass(f"Password for {NEW_USER}: ")
        if len(pwd.strip()) < 8:
            printError(f"Password must be at least 8 characters")
            continue
        confirm = getpass.getpass("Confirm password: ")
        if pwd == confirm:
            return pwd
        printError("Passwords do not match. Please try again.")




def sshKeyExists():
    auth_file = f"/home/{NEW_USER}/.ssh/authorized_keys"
    return os.path.exists(auth_file) and os.path.getsize(auth_file) > 0

def sshSetup():
    printHead("SSH Key Setup")
    if sshKeyExists():
        printWarning(f"SSH Key already exists. Skipping setup.")
        return
    ssh_dir = f"/home/{NEW_USER}/.ssh"
    auth_file = f"{ssh_dir}/authorized_keys"
    os.makedirs(ssh_dir, exist_ok=True)
    printDot(f"Paste your SSH public key (Ctrl+D to finish):")
    key_lines = []
    try:
        while True:
            keyline = input()
            key_lines.append(keyline)
    except EOFError:
        pass
    pub_key = "\n".join(key_lines).strip()
    if not pub_key:
        printError("No SSH key provided. Skipping SSH setup.")
        sys.exit(1)
    with open(auth_file, "w") as f:
        f.write(pub_key + "\n")
    run(f"chmod 0700 {ssh_dir}")
    run(f"chmod 0600 {auth_file}")
    run(f"chown -R {NEW_USER}:{NEW_USER} {ssh_dir}")
    printSuccess(f"SSH Key setup completed.")

def updateSystem():
    printHead("Updating System")
    run("apt update && apt full-upgrade -y")
    run("apt autoremove -y && apt clean")
    printSuccess("System updated")

def userExists():
    return run(f"id {NEW_USER}", check=False, capture=True).returncode == 0
