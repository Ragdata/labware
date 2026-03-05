#!/usr/bin/env bash
####################################################################
# pyenv.sh
####################################################################
# Ragdata's Dotfiles - Dotfile Installer
#
# File:         pyenv.sh
# Author:       Ragdata
# Date:         01/03/2026
# License:      MIT License
# Repository:	https://github.com/Ragdata/.dotfiles
# Copyright:    Copyright © 2026 Redeyed Technologies
####################################################################
# FUNCTIONS
####################################################################
pyenv::install()
{
	curl -fsSL https://pyenv.run | bash
}

pyenv::config()
{
	{
		echo "export PYENV_ROOT=\"$HOME/.pyenv\""
		echo "[[ -d $PYENV_ROOT/bin ]] && export PATH=\"$PYENV_ROOT/bin:$PATH\""
		echo "eval $(pyenv init - bash)"
	} >> ~/.bashrc
	{
		echo "export PYENV_ROOT=\"$HOME/.pyenv\""
		echo "[[ -d $PYENV_ROOT/bin ]] && export PATH=\"$PYENV_ROOT/bin:$PATH\""
		echo "eval $(pyenv init - bash)"
	} >> ~/.profile
}

pyenv::plugins()
{
	git clone https://github.com/pyenv/pyenv-virtualenv.git "$HOME/.pyenv/plugins/pyenv-virtualenv"
	echo "eval $(pyenv virtualenv-init -)" >> ~/.bashrc
	git clone https://github.com/pyenv/pyenv-update.git "$HOME/.pyenv/plugins/pyenv-update"
}

pyenv::uninstall()
{
	rm -rf ~/.pyenv

	sed -i "/export PYENV_ROOT/d" ~/.bashrc
	sed -i "/export PATH=\"$PYENV_ROOT/bin:$PATH\"/d" ~/.bashrc
	sed -i "/eval \"\$(pyenv init - bash)\"/d" ~/.bashrc
	sed -i "/eval \"\$(pyenv virtualenv-init -)\"/d" ~/.bashrc
	sed -i "/export PYENV_ROOT/d" ~/.profile
	sed -i "/export PATH=\"\$PYENV_ROOT\/bin:\$PATH\"/d" ~/.profile
	sed -i "/eval \"\$(pyenv init - bash)\"/d" ~/.profile

}
