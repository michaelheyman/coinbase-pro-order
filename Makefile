PACKAGE_NAME=cbproorder
READMES=README.md terraform/README.md

.PHONY: clean
clean: ## Clean all Python artifacts
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -f .coverage
	rm -rf .mypy_cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

.PHONY: lint
lint: lint/flake8 ## Check style

.PHONY: lint/flake8
lint/flake8: ## Check style with flake8
	flake8 ${PACKAGE_NAME}

.PHONY: format
format: format/black format/isort ## Format files

.PHONY: format/black
format/black: ## Format with black
	black ${PACKAGE_NAME} tests

format/isort: ## Reorder imports with isort
	isort ${PACKAGE_NAME} tests

.PHONY: pre-commit
pre-commit: ## Run pre-commit on all files
	pre-commit run --all-files

.PHONY: test-coverage
test-coverage: ## Run test coverage tool
	python -m pytest \
	--cov-report term-missing \
	--cov=${PACKAGE_NAME} tests/

.PHONY: readme
readme: readme/lint readme/format ## Apply READMEs formatting and linting

.PHONY: readme/lint
readme/lint: ## Lint READMEs
	npx -y markdownlint-cli2 --fix ${READMES}

.PHONY: readme/format
readme/format: ## Format READMEs
	npx -y doctoc --github ${READMES}

.PHONY: run
run: ## Run the application
	ENABLE_STANDARD_LOG_FORMAT=${ENABLE_STANDARD_LOG_FORMAT:true} python -m ${PACKAGE_NAME}

.PHONY: test
test: ## Run tests
	python -m pytest -vv

.DEFAULT_GOAL := help
help:
	@grep -E '^[^: ]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
