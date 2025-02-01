SHELL :=/bin/bash
CWD := $(PWD)
TMP_PATH := $(CWD)/.tmp
VENV_PATH := $(CWD)/venv
PYTHON_VERSION = python3.10
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
	@if ! command -v $(PYTHON_VERSION) > /dev/null; then \
		echo "❌ Error: $(PYTHON_VERSION) not found in your system."; \
		echo "Please specify the python version available in your system that is >= 'Python3.9'"; \
		echo ">>> Example:"; \
		echo "make venv PYTHON_VERSION=python3.11"; \
		exit 0; \
	else \
		echo "📦 Creating virtual env at: $(VENV_PATH)"; \
		$(PYTHON_VERSION) -m venv venv; \
		echo -e "✅ Done.\n\n🎉 Run the following commands to activate the virtual environment:\n ➡️ source $(VENV_PATH)/bin/activate\n\nThen run the following command to install dependencies:\n ➡️ make setup"; \
	fi

format: # Format auto-fixable linting issues
	@ruff check good_first_issues --fix

check: # Ruff check for formatting issues
	@ruff check .
	@echo "✅ Check complete!"

setup: # Setup local development environment
	@pip install -e .[dev]

help: # Show this help
	@egrep -h '\s#\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
