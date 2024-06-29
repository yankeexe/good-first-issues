SHELL :=/bin/bash
CWD := $(PWD)
TMP_PATH := $(CWD)/.tmp
VENV_PATH := $(CWD)/venv
docker_image := good-first-issues

.PHONY: test clean
.DEFAULT_GOAL := help


build: # Build Docker image for CLI
	@docker build -t $(docker_image) .

build.if:
	@if [ "$$(docker images -q $(docker_image) 2> /dev/null)" = "" ]; then \
		$(MAKE) -s build; \
	fi

clean: # Clean cache files
	@rm -rf $(TMP_PATH) __pycache__ .pytest_cache
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -delete

test: # Run pytest
	@pytest -vvv

venv: # Create a virtual environment
	@python3 -m venv venv

format: # Format code base with black
	@ruff format good_first_issues

check: # Check for formatting issues with black
	@black --check --diff .

setup: # Setup local development environment
	@pip install -e .[dev]

lint: # Run linters
	@ruff format --check good_first_issues

help: # Show this help
	@egrep -h '\s#\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
