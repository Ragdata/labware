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
import subprocess, sys

from pathlib import Path


def pyenvCheck():
	pyenv_path = Path.home() / ".pyenv"
	if pyenv_path.exists():
		print("Pyenv is already installed.")
		return True
	else:
		print("Pyenv is not installed.")
		return False

def pyenvInstall(check=True):
	try:
		result = subprocess.run("curl -fsSL https://pyenv.run | bash", shell=True, check=check, text=True, capture_output=False, input=None)
		subprocess.run("echo 'export PYENV_ROOT=\"$HOME/.pyenv\"' >> ~/.bashrc")
		subprocess.run("echo '[[ -d $PYENV_ROOT/bin ]] && export PATH=\"$PYENV_ROOT/bin:$PATH\"' >> ~/.bashrc")
		subprocess.run("echo 'eval \"$(pyenv init - bash)\"' >> ~/.bashrc")
		profile = Path.home() / ".profile"
		if not profile.exists():
			profile.touch()
		subprocess.run("echo 'export PYENV_ROOT=\"$HOME/.pyenv\"' >> ~/.profile")
		subprocess.run("echo '[[ -d $PYENV_ROOT/bin ]] && export PATH=\"$PYENV_ROOT/bin:$PATH\"' >> ~/.profile")
		subprocess.run("echo 'eval \"$(pyenv init - bash)\"' >> ~/.profile")

		# Install Plugins
		plugins = input("Do you want to install pyenv plugins? (y/n): ").lower()
		if plugins == "y":
			subprocess.run("git clone https://github.com/pyenv/pyenv-virtualenv.git Path.home() / '.pyenv/plugins/pyenv-virtualenv'")
			subprocess.run("echo 'eval \"$(pyenv virtualenv-init -)\"' >> ~/.bashrc")
			subprocess.run("git clone https://github.com/pyenv/pyenv-update.git Path.home() / '.pyenv/plugins/pyenv-update'")
		return result
	except subprocess.CalledProcessError as e:
		print(e.output)
		if check:
			sys.exit(1)

def pyenvUninstall(check=True):
	try:
		result = subprocess.run("rm -rf ~/.pyenv", shell=True, check=check, text=True, capture_output=False, input=None)
		subprocess.run("sed -i '/export PYENV_ROOT/d' ~/.bashrc")
		subprocess.run("sed -i '/export PATH=\"\$PYENV_ROOT\/bin:\$PATH\"/d' ~/.bashrc")
		subprocess.run("sed -i '/eval \"\$(pyenv init - bash)\"/d' ~/.bashrc")
		subprocess.run("sed -i '/eval \"\$(pyenv virtualenv-init -)\"/d' ~/.bashrc")
		subprocess.run("sed -i '/export PYENV_ROOT/d' ~/.profile")
		subprocess.run("sed -i '/export PATH=\"\$PYENV_ROOT\/bin:\$PATH\"/d' ~/.profile")
		subprocess.run("sed -i '/eval \"\$(pyenv init - bash)\"/d' ~/.profile")
		return result
	except subprocess.CalledProcessError as e:
		print(e.output)
		if check:
			sys.exit(1)

def pyenvHelp():
	pass
