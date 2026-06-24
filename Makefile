.PHONY: help install install-dev install-web install-mobile test test-cov test-v lint format type-check clean run-web run-mobile run-all docs

help:
	@echo "Natural Language Todo App - Makefile Commands"
	@echo ""
	@echo "Installation:"
	@echo "  make install           Install all dependencies"
	@echo "  make install-dev       Install with dev dependencies"
	@echo "  make install-web       Install web interface only"
	@echo "  make install-mobile    Install mobile interface only"
	@echo ""
	@echo "Development:"
	@echo "  make test              Run tests"
	@echo "  make test-cov          Run tests with coverage report"
	@echo "  make test-v            Run tests in verbose mode"
	@echo "  make lint              Run linters (flake8, mypy)"
	@echo "  make format            Format code (black, isort)"
	@echo "  make type-check        Run type checking with mypy"
	@echo ""
	@echo "Running:"
	@echo "  make run-web           Run web interface (Streamlit)"
	@echo "  make run-mobile        Run mobile interface (Kivy)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean             Remove build artifacts and cache"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

install-web:
	pip install -r requirements-web.txt

install-mobile:
	pip install -r requirements-mobile.txt

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=todo_core --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

test-v:
	pytest tests/ -vv

lint:
	flake8 todo_core todo_web todo_mobile tests --max-line-length=100
	@echo "Linting complete!"

format:
	black todo_core todo_web todo_mobile tests
	isort todo_core todo_web todo_mobile tests
	@echo "Code formatted!"

type-check:
	mypy todo_core --ignore-missing-imports

run-web:
	streamlit run todo_web/app.py

run-mobile:
	python -m todo_mobile

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	@echo "Cleaned!"

all-checks: lint type-check test-cov
	@echo "All checks passed!"
