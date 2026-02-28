MAKEFLAGS += --silent

.ONESHELL:

SHELL := /bin/bash

CUSTOM := "$(HOME)/.dotfiles/custom"
SYSDIR := "$(HOME)/.labware/sys"

.PHONY: clean check install uninstall debug

MODE := $(if $(DEV),dev,prod)
USER := $(shell whoami)
UID  := $(shell id -u)
PWD  := $(shell pwd)


check:
	@echo "Running in $(MODE) mode."
	@echo "Running as $(USER) with UID $(UID)"

debug:
	@echo "DEBUG: PWD=$(PWD)"
	@echo "DEBUG: MODE=$(MODE)"
	@echo "DEBUG: CUSTOM=$(CUSTOM)"
	@echo "DEBUG: SYSDIR=$(SYSDIR)"
	@echo "DEBUG: VIRTUAL_ENV=$(VIRTUAL_ENV)"
	@echo "DEBUG: PATH=$(PATH)"
	@echo "DEBUG: SHELL=$(SHELL)"
	@echo "DEBUG: SHELLFLAGS=$(SHELLFLAGS)"
	@echo "DEBUG: MAKEFLAGS=$(MAKEFLAGS)"

install:
	@echo
	@if $(UID) != 0; then
		@echo "This command MUST be run as root or with sudo privileges"
		@exit 1
	fi
	@echo "Installing Labware in $(MODE) mode..."
	@if [ "$(MODE)" == "dev" ]; then
		pip install -e . -q
	else
		pip install . -q
	fi
	@echo "Labware installed successfully."
	@if [ "$(MODE)" == "dev" ]; then
		@lab install --debug
	else
		@lab install
	fi

uninstall:
	@echo

clean:
	@echo

test:
	@echo

