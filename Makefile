.PHONY: help install update test lint format

# Default target
help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

install: ## Set up the poetry environment
	@poetry install

update: ## Update the poetry environment
	@poetry update

test: ## Run tests
	@poetry run pytest

format: ## Format sources
	@poetry run black .
	@poetry run isort .
	@poetry run ruff check . --fix

lint: ## Run linters
	@poetry run pyright .
	@poetry run ruff check .
	@poetry run mypy .
	@poetry run black --check .
	@poetry run isort --check .