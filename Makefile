PACKAGE_NAME=cbproorder

.PHONY: lint
lint: lint/black lint/flake8 ## Check style

.PHONY: lint/black
lint/black: ## Check style with black
	black ${PACKAGE_NAME} tests

.PHONY: lint/flake8
lint/flake8: ## Check style with flake8
	flake8 ${PACKAGE_NAME}

.PHONY: pre-commit
pre-commit: ## Run pre-commit on all files
	pre-commit run --all-files

.PHONY: test-coverage
test-coverage: ## Run test coverage tool
	python -m pytest \
	--cov-report term-missing \
	--cov=${PACKAGE_NAME} tests/

.PHONY: run
run: ## Run the application
	python -m ${PACKAGE_NAME}

.PHONY: test
test: ## Run tests
	python -m pytest -vv

.DEFAULT_GOAL := help
help:
	@grep -E '^[^: ]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
