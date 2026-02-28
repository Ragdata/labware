MAKEFLAGS += --silent

.ONESHELL:

SHELL := /bin/bash

CUSTOM := "$(HOME)/.dotfiles/custom"
SYSDIR := "$(HOME)/.labware/sys"

MODE := $(if $(DEV),dev,prod)
USER := $(shell whoami)
UID  := $(shell id -u)
PWD  := $(shell pwd)


.PHONY: clean check install uninstall debug


clean:
	echo

debug:
	echo "Running in $(MODE) mode."
	echo "Running as $(USER) with UID $(UID)"
	echo "DEBUG: PWD=$(PWD)"
	echo "DEBUG: MODE=$(MODE)"
	echo "DEBUG: CUSTOM=$(CUSTOM)"
	echo "DEBUG: SYSDIR=$(SYSDIR)"
	echo "DEBUG: VIRTUAL_ENV=$(VIRTUAL_ENV)"
	echo "DEBUG: PATH=$(PATH)"
	echo "DEBUG: SHELL=$(SHELL)"
	echo "DEBUG: SHELLFLAGS=$(SHELLFLAGS)"
	echo "DEBUG: MAKEFLAGS=$(MAKEFLAGS)"

install:
	echo
	# Check that a suitable environment exists
	if [ "$(UID)" != 0 ]; then echo "This command MUST be run as root or with sudo privileges"; exit 1; fi
	if [ -z "$(which python)" ]; then echo "This package requires python version 3.12+ - install and try again"; exit 1; fi
	if [ -z "$(which pip)" ]; then echo "This package requires pip - install and try again"; exit 1; fi
	if [ ! -z "$VIRTUAL_ENV" ]; then echo "This package needs to be run in a virtual environment - create env and try again"; exit 1; fi

	echo "Installing Labware in $(MODE) mode..."
	try:
		if [ "$(MODE)" == "dev" ]; then pip install -e . -q; else pip install . -q; fi
	except Exception as e:
		raise Exception(e)
		echo "There was a problem installing the Labware module"
		exit 1
	echo "Labware installed successfully."

	# Execute Labware Installer
	# if [ "$(MODE)" == "dev" ]; then
	# 	lab install --debug
	# else
	# 	lab install
	# fi

test:
	echo

uninstall:
	echo
