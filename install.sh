#!/usr/bin/env bash
####################################################################
# install.sh
####################################################################
# File:         install.sh
# Author:       Ragdata
# Date:         13/03/2026
# License:      MIT License
# Repository:	https://github.com/Ragdata/.dotfiles
# Copyright:    Copyright © 2026 Redeyed Technologies
####################################################################
# PRE-FLIGHT
####################################################################

. vendor/progressbar

# COLORS (minimal)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# TOOLS
tools=("make" "build-essential" "libssl-dev" "zlib1g-dev" "libbz2-dev" "libreadline-dev" "libsqlite3-dev" "curl" "wget" "git" "libncursesw5-dev" "xz-utils" "tk-dev" "libxml2-dev" "libxmlsec1-dev" "libffi-dev" "liblzma-dev")

# PROGRESSBAR
REMAIN=" "
StepsDone=0
TotalSteps=$((${#tools[@]}+3))

# PATHS
PYENV_ROOT="$HOME/.pyenv"

export DEBIAN_FRONTEND=noninteractive

####################################################################
# PROCESS
####################################################################
if ! sudo -v; then
	echo -e "${RED}This script requires sudo privileges${NC}"
	exit 1
fi

if ! grep -q "Ubuntu 24" /etc/os-release 2> /dev/null; then
	echo -e "${RED}This script requires Ubuntu 24.04 LTS${NC}"
	exit 1
fi

clear

bar::start

echo -e "${YELLOW}Updating System ...${NC}"
bar::status_changed $((${StepsDone})) $TotalSteps
apt update -qq
bar::status_changed $(($StepsDone+1)) $TotalSteps
echo -e "${YELLOW}Upgrading System ...${NC}"
apt full-upgrade -y -qq
bar::status_changed $(($StepsDone+1)) $TotalSteps
echo -e "${YELLOW}Installing Build Tools ...${NC}"
for tool in "${tools[@]}"; do
	if ! apt install -y "$tool" &> /dev/null; then
		echo -e "${YELLOW}Failed to install '$tool'${NC}"
	else
		echo -e "${GREEN}Successfully installed '$tool'${NC}"
	fi
	StepsDone=$((${StepsDone:-2}+1))
	bar::status_changed $StepsDone $TotalSteps
done
echo -e "${YELLOW}Cleaning Up ...${NC}"
apt autoremove -y -qq && apt clean -qq
bar::status_changed $(($StepsDone+1)) $TotalSteps

bar::stop

if [ ! -d "$HOME/.pyenv" ]; then
	echo -e "${YELLOW}Installing PYENV ...${NC}"
	if curl -fsSL https://pyenv.run | bash; then
		{
			echo
			echo '# Pyenv Configuration';
			echo 'export PYENV_ROOT="$HOME/.pyenv"';
			echo '[[ -d $PYENV_ROOT/bin ]] && export PATH=$PYENV_ROOT/bin:$PATH';
			echo 'eval "$(pyenv init - bash)"';
			echo '# eval "$(pyenv virtualenv-init -)"';
		} >> ~/.bashrc
		{
			echo
			echo '# Pyenv Configuration';
			echo 'export PYENV_ROOT="$HOME/.pyenv"';
			echo '[[ -d $PYENV_ROOT/bin ]] && export PATH=$PYENV_ROOT/bin:$PATH';
			echo 'eval "$(pyenv init - bash)"';
			echo '# eval "$(pyenv virtualenv-init -)"';
		} >> ~/.profile
	else
		echo -e "${RED}Failed to install pyenv${NC}"
		exit 1
	fi
fi

echo -e "${YELLOW}Reloading Shell ...${NC}"
if ! source ~/.bashrc; then
	echo -e "${RED}Failed to reload shell${NC}"
	exit 1
else
	echo -e "${GREEN}Successfully reloaded shell${NC}"
fi

echo -e "${YELLOW}Installing Python ...${NC}"
if ! pyenv install 3.14:latest; then
	echo -e "${RED}Failed to install python${NC}"
	exit 1
else
	echo -e "${GREEN}Successfully installed python${NC}"
fi
if ! pyenv global 3.14; then
	echo -e "${RED}Failed to set global python version${NC}"
	exit 1
else
	echo -e "${GREEN}Successfully set global python version${NC}"
fi
echo -e "${YELLOW}Setting Up Virtual Environment ...${NC}"
if [ ! -d "$HOME/.pyenv/versions/labenv" ]; then
	if pyenv virtualenv labenv; then
		echo -e "${GREEN}Successfully created virtual environment${NC}"
	else
		echo -e "${RED}Failed to create virtual environment${NC}"
		exit 1
	fi
fi

pyenv activate labenv

if "$DEV"; then
	pip install -e . -q
	lab install --debug
else
	pip install . -q
	lab install
fi
