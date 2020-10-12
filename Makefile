SHELL :=/bin/bash
CWD := $(PWD)
TMP_PATH := $(CWD)/.tmp
VENV_PATH := $(CWD)/venv

.PHONY: test clean

clean:
	@rm -rf $(TMP_PATH) __pycache__ .pytest_cache
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -delete

test:
	@pytest -vvv

venv:
	@python3 -m venv venv

format:
	@black .

check:
	@black --check --diff .

setup:
	@pip install -e .[dev]
