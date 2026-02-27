#!/usr/bin/env bash
####################################################################
# prompts.bash
####################################################################
# Author:       Ragdata
# Date:         22/08/2024
# License:      MIT License
# Repository:	https://github.com/Ragdata/.dotfiles
# Copyright:    Copyright © 2024 Redeyed Technologies
####################################################################

[ -z "$DOTFILES_PROMPT" ] && DOTFILES_PROMPT="default"

source "$HOME/.bashrc.d/prompts/${DOTFILES_PROMPT,,}.bash"
