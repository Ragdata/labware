MAKEFLAGS += --silent

.ONESHELL:

SHELL := /bin/bash

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
	./scr/install.sh

test:
	echo

uninstall:
	echo
	pyenv uninstall labenv

