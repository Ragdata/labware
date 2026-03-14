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
# FUNCTIONS
####################################################################
if [[ ! "$DEV" ]]; then
	apt update
	apt full-upgrade -y
	apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl wget git libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
	apt autoremove -y && apt clean
fi
if [[ ! -d "\$HOME/.pyenv" ]]; then
	curl -fsSL https://pyenv.run | bash
	{
		echo "export PYENV_ROOT=\"\$HOME/.pyenv\"";
		echo "[[ -d \$PYENV_ROOT/bin ]] && export PATH=\"\$PYENV_ROOT/bin:\$PATH\"";
		echo "eval \$(pyenv init - bash)";
	} >> ~/.bashrc
	{
		echo "export PYENV_ROOT=\"\$HOME/.pyenv\"";
		echo "[[ -d \$PYENV_ROOT/bin ]] && export PATH=\"\$PYENV_ROOT/bin:\$PATH\"";
		echo "eval \$(pyenv init - bash)";
	} >> ~/.profile;
	git clone https://github.com/pyenv/pyenv-virtualenv.git "$HOME/.pyenv/plugins/pyenv-virtualenv"
	echo "eval \$(pyenv virtualenv-init -)" >> ~/.bashrc
	git clone https://github.com/pyenv/pyenv-update.git "$HOME/.pyenv/plugins/pyenv-update"
	source ~/.bashrc
	pyenv install 3:latest
	pyenv global 3
fi
if [[ ! -L "$HOME/.pyenv/versions/labenv" ]]; then
	pyenv virtualenv labenv
fi
if [[ "$DEV" ]]; then
	pyenv activate labenv
	pip install -e . -q
	lab install --debug
else
	pyenv activate labenv
	pip install . -q
	lab install
fi
