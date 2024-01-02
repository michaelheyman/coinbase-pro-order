FUNCTION_DEPOSIT_PORT=8081
FUNCTION_ORDERS_PORT=8082
PACKAGE_NAME=cbproorder
READMES=README.md terraform/README.md

# Load .env variables into Makefile if the file exists
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

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

.PHONY: mypy
mypy: ## Run the mypy type checker
	mypy . --ignore-missing-imports --disallow-untyped-defs --exclude '^tests/.*'

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

.PHONY: run_deposit_function
run_deposit_function: ## Run the deposit function
	COINBASE_API_BASE_URL=http://localhost:3000 \
	COINBASE_API_KEY=your_api_key \
	COINBASE_SECRET_KEY=your_api_secret \
	LOGGING_LEVEL=DEBUG \
	TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN} \
	TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID} \
	functions-framework --target=coinbase_deposit --signature-type=event --debug --port=${FUNCTION_DEPOSIT_PORT}

.PHONY: run_orders_function
run_orders_function: ## Run the orders function
	COINBASE_API_BASE_URL=http://localhost:3000 \
	COINBASE_API_KEY=your_api_key \
	COINBASE_SECRET_KEY=your_api_secret \
	LOGGING_LEVEL=DEBUG \
	TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN} \
	TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID} \
	functions-framework --target=coinbase_orders --signature-type=event --debug --port=${FUNCTION_ORDERS_PORT}

.PHONY: run_mockoon
run_mockoon: ## Run mockoon
	mockoon-cli start --data ./mock_servers/coinbase/environment.json --port 3000 --log-transaction

.PHONY: test
test: ## Run tests
	python -m pytest -vv

.PHONY: up
up: ## Run docker compose
	docker compose up --build

.DEFAULT_GOAL := help
help:
	@grep -E '^[^: ]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
