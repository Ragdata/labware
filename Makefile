MAKEFLAGS += --silent

.ONESHELL:

SHELL := /bin/bash

CUSTOM := "$(HOME)/.dotfiles/custom"
SYSDIR := "$(HOME)/.labware/sys"

.PHONY: clean check install uninstall debug

MODE := $(if $(DEV),dev,prod)

check:
	@echo "Running in $(MODE) mode."

debug:
	@echo "DEBUG: MODE=$(MODE)"
	@echo "DEBUG: CUSTOM=$(CUSTOM)"
	@echo "DEBUG: SYSDIR=$(SYSDIR)"
	@echo "DEBUG: VIRTUAL_ENV=$(VIRTUAL_ENV)"
	@echo "DEBUG: PATH=$(PATH)"
	@echo "DEBUG: SHELL=$(SHELL)"
	@echo "DEBUG: SHELLFLAGS=$(SHELLFLAGS)"
	@echo "DEBUG: MAKEFLAGS=$(MAKEFLAGS)"

setup:
	@echo
	@mkdir -p "$HOME/.dotfiles/custom" "$HOME/.labware/sys"

install:
	@echo
	@echo "Installing Labware in $(MODE) mode..."
	@if [ "$(MODE)" == "dev" ]; then
		$(VENV_PATH)/bin/pip install -e . -q
	else
		$(VENV_PATH)/bin/pip install . -q
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

