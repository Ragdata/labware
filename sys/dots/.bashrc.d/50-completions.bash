#!/usr/bin/env bash
####################################################################
# completions.bash
####################################################################
# Author:       Ragdata
# Date:         22/08/2024
# License:      MIT License
# Repository:	https://github.com/Ragdata/.dotfiles
# Copyright:    Copyright © 2024 Redeyed Technologies
####################################################################

# Install bash-completion if not already installed
if ! pkg::installed "bash-completion"; then 
    sudo apt install -y bash-completion
fi
# Load bash-completion if available
if [ -f /etc/bash_completion ]; then
    source /etc/bash_completion
fi
# Create the bash-completion directory if it doesn't exist
if [[ ! -d "$HOME"/.local/share/bash-completion/completions ]]; then
    mkdir -p "$HOME"/.local/share/bash-completion/completions
fi
# Install Docker completion if not already installed
if [[ ! -f "$HOME"/.local/share/bash-completion/completions/docker ]]; then
    docker completion bash > "$HOME"/.local/share/bash-completion/completions/docker
fi
