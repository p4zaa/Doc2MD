# Makefile for Doc2MD

.PHONY: help install install-dev test test-cov clean lint format docs build publish

help:  ## Show this help message
	@echo "Doc2MD - Web Document to Markdown Converter"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package in development mode
	pip install -e .

install-dev:  ## Install the package with development dependencies
	pip install -e ".[dev]"

test:  ## Run the test suite
	python -m pytest tests/ -v

test-exclude:  ## Run exclude URLs tests specifically
	python -m pytest tests/test_exclude_urls.py -v

test-cov:  ## Run tests with coverage report
	python -m pytest tests/ --cov=doc2md --cov-report=html --cov-report=term

clean:  ## Clean up generated files and caches
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name "docs" -exec rm -rf {} +
	find . -type d -name "example_output" -exec rm -rf {} +
	find . -type d -name "limited_depth_output" -exec rm -rf {} +
	find . -type d -name "batch_output" -exec rm -rf {} +
	find . -type d -name "error_test_output" -exec rm -rf {} +

lint:  ## Run linting checks
	flake8 doc2md/ tests/ examples/ cli.py setup.py
	mypy doc2md/ tests/ examples/ cli.py setup.py

format:  ## Format code with black
	black doc2md/ tests/ examples/ cli.py setup.py

docs:  ## Generate documentation
	python examples/basic_usage.py
	python examples/advanced_usage.py

build:  ## Build the package
	python setup.py sdist bdist_wheel

publish:  ## Publish to PyPI (requires twine)
	twine upload dist/*

check:  ## Run all checks (lint, test, format)
	@echo "Running all checks..."
	@make lint
	@make test
	@make format

demo:  ## Run a demo conversion (replace with actual URL)
	@echo "Running demo conversion..."
	@echo "Note: Replace the URL in examples/basic_usage.py with a real site"
	python examples/basic_usage.py

install-cli:  ## Install CLI tool globally
	pip install -e ".[cli]"

uninstall:  ## Uninstall the package
	pip uninstall doc2md -y

reset: clean install-dev  ## Clean and reinstall everything

.PHONY: version
version:  ## Show current version
	@python -c "import doc2md; print(doc2md.__version__)"

.PHONY: requirements
requirements:  ## Update requirements.txt from setup.py
	pip install pip-tools
	pip-compile setup.py --output-file requirements.txt

.PHONY: requirements-dev
requirements-dev:  ## Update dev requirements
	pip install pip-tools
	pip-compile setup.py --extra=dev --output-file requirements-dev.txt
