SHELL:=/bin/bash
VERSION=0x03

.PHONY: install
install:
	@python3 -m venv venv
	@source venv/bin/activate && pip3 install -r requirements.txt

.PHONY: help
	@source venv/bin/activate && python3 collect.py -h