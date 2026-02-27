#!/usr/bin/env bash
####################################################################
# aliases.bash
####################################################################
# Author:       Ragdata
# Date:         22/08/2024
# License:      MIT License
# Repository:	https://github.com/Ragdata/.dotfiles
# Copyright:    Copyright © 2024 Redeyed Technologies
####################################################################

# general aliases
alias reload='dot::reload'
alias relog='dot::relog'
alias daemon-reload='sudo systemctl daemon-reload'

# some more ls aliases
alias ll='ls -avlF --color --group-directories-first'
alias la='ls -A'
alias l='ls -CF'

# docker aliases
alias dkstart='sudo systemctl start docker'
alias dkstop='sudo systemctl stop docker.socket; sudo systemctl stop docker'
alias dkstat='sudo systemctl status docker'
alias dkstatus='dstat'
alias dkrestart='sudo systemctl restart docker'

alias dcup='docker compose -f "${1:-docker-compose.yml}" up -d'
alias dcdown='docker compose -f "${1:-docker-compose.yml}" down'

# python aliases
alias py='python3'
alias pip='pip3'
alias labenv='source ~/.venv/labenv/bin/activate'

# git aliases
alias g='git'

