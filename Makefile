MAKEFLAGS += --silent

.ONESHELL:

SHELL := /bin/bash

REPODIR := "$(PWD)"
BASEDIR := "$(HOME)/.labware"

MODE := $(if $(DEV),dev,prod)

.PHONY: clean check install uninstall debug


clean:
	echo

debug:
	echo "Running in $(MODE) mode."
	echo "Running as $(USER) with UID $(UID)"
	echo "DEBUG: MODE=$(MODE)"
	echo "DEBUG: REPODIR=$(PWD)"
	echo "DEBUG: BASEDIR=$(BASEDIR)"
	echo "DEBUG: VIRTUAL_ENV=$(VIRTUAL_ENV)"
	echo "DEBUG: PATH=$(PATH)"
	echo "DEBUG: SHELL=$(SHELL)"
	echo "DEBUG: SHELLFLAGS=$(SHELLFLAGS)"
	echo "DEBUG: MAKEFLAGS=$(MAKEFLAGS)"

install:
	if [[ "$(MODE)" != "dev" ]]; then
		apt update
		apt full-upgrade -y
		apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl wget git libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
		apt autoremove -y && apt clean
	fi

	if [[ ! -d "$(HOME)/.pyenv" ]]; then

	fi
	if [[ "$(MODE)" == "dev" ]]; then
		pip install -e . -q
		lab install --debug
	else
		pip install . -q
		lab install
	fi

test:
	echo

uninstall:
	echo
