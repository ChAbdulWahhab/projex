.PHONY: help install install-dev test coverage lint format clean build publish setup-git-hooks run-example

help:
	@echo "Projex - Development Commands"
	@echo ""
	@echo "  make install        Install package in production mode"
	@echo "  make install-dev    Install package in development mode"
	@echo "  make test           Run tests"
	@echo "  make coverage       Run tests with coverage report"
	@echo "  make lint           Run code linting"
	@echo "  make format         Format code with black"
	@echo "  make clean          Clean build artifacts"
	@echo "  make build          Build distribution packages"
	@echo "  make publish        Publish to PyPI"
	@echo "  make run-example    Create example project"
	@echo "  make setup-git-hooks Setup pre-commit git hooks"

install:
	pip install .

install-dev:
	pip install -e .
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

coverage:
	pytest --cov=projex --cov-report=html --cov-report=term tests/
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	flake8 projex/
	mypy projex/

format:
	black projex/ tests/
	isort projex/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python setup.py sdist bdist_wheel

publish: build
	twine upload dist/*

run-example:
	projex create example-api --template fastapi --author "Test User" --no-git --no-venv

setup-git-hooks:
	@echo "Setting up git hooks..."
	@echo "#!/bin/sh" > .git/hooks/pre-commit
	@echo "make format" >> .git/hooks/pre-commit
	@echo "make lint" >> .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
	@echo "Git hooks installed!"
