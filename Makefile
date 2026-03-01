MAKEFLAGS += --silent

.ONESHELL:

SHELL := /bin/bash

CUSTOM := "$(HOME)/.dotfiles/custom"
SYSDIR := "$(HOME)/.labware/sys"

MODE := $(if $(DEV),dev,prod)

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
	
#	try:
#		if [ "$(MODE)" == "dev" ]; then pip install -e . -q; else pip install . -q; fi
#	except Exception as e:
#		raise Exception(e)
#		echo "There was a problem installing the Labware module"
#		exit 1

#	# Execute Labware Installer
#	if [ "$(MODE)" == "dev" ]; then
#		lab install --debug
#	 else
#		lab install
#	fi

test:
	echo

uninstall:
	echo
