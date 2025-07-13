.PHONY: help test unit integration performance edge all coverage lint format clean install dev

# Default target
help:
	@echo "HR System Backend - Available Commands:"
	@echo ""
	@echo "Testing:"
	@echo "  test        - Run all tests with coverage"
	@echo "  unit        - Run unit tests only"
	@echo "  integration - Run integration tests only"
	@echo "  performance - Run performance tests only"
	@echo "  edge        - Run edge case tests only"
	@echo "  coverage    - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code with black"
	@echo "  imports     - Sort imports with isort"
	@echo ""
	@echo "Development:"
	@echo "  install     - Install dependencies"
	@echo "  dev         - Install development dependencies"
	@echo "  clean       - Clean up generated files"
	@echo "  migrate     - Run database migrations"
	@echo "  server      - Start development server"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -e .

# Install development dependencies
dev:
	@echo "Installing development dependencies..."
	pip install -e ".[dev]"

# Run all tests
test:
	@echo "Running all tests..."
	python -m pytest --cov=candidate --cov=core --cov-report=html --cov-report=term-missing --cov-fail-under=80 -v

# Run unit tests
unit:
	@echo "Running unit tests..."
	python -m pytest candidate/tests.py::CandidateModelTest candidate/tests.py::StatusHistoryModelTest candidate/tests.py::CandidateSerializerTest candidate/tests.py::PermissionTest -v

# Run integration tests
integration:
	@echo "Running integration tests..."
	python -m pytest candidate/tests.py::CandidateAPITest candidate/tests.py::StatusHistoryAPITest -v

# Run performance tests
performance:
	@echo "Running performance tests..."
	python -m pytest candidate/tests.py::PerformanceTest -v

# Run edge case tests
edge:
	@echo "Running edge case tests..."
	python -m pytest candidate/tests.py::EdgeCaseTest -v

# Run tests with coverage
coverage:
	@echo "Running tests with coverage..."
	python -m pytest --cov=candidate --cov=core --cov-report=html --cov-report=term-missing --cov-report=xml -v

# Run code linting
lint:
	@echo "Running code linting..."
	flake8 candidate core --max-line-length=88 --count --statistics

# Format code
format:
	@echo "Formatting code..."
	black candidate core --line-length=88

# Sort imports
imports:
	@echo "Sorting imports..."
	isort candidate core

# Clean up generated files
clean:
	@echo "Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov .pytest_cache
	rm -rf build dist

# Run database migrations
migrate:
	@echo "Running database migrations..."
	python manage.py migrate

# Start development server
server:
	@echo "Starting development server..."
	python manage.py runserver

# Run tests in parallel
test-parallel:
	@echo "Running tests in parallel..."
	python -m pytest -n auto --cov=candidate --cov=core --cov-report=term-missing -v

# Run security checks
security:
	@echo "Running security checks..."
	bandit -r candidate -f json -o bandit-report.json

# Run all quality checks
quality: lint format imports
	@echo "All quality checks completed!"

# Quick test (fastest subset)
quick:
	@echo "Running quick tests..."
	python -m pytest candidate/tests.py::CandidateModelTest::test_candidate_creation -v

# Test with verbose output
test-v:
	@echo "Running tests with verbose output..."
	python -m pytest --cov=candidate --cov=core --cov-report=term-missing -vvv

# Test with debug output
test-debug:
	@echo "Running tests with debug output..."
	python -m pytest --cov=candidate --cov=core --cov-report=term-missing -vvv --tb=long

# Generate test report
report:
	@echo "Generating test report..."
	python -m pytest --cov=candidate --cov=core --cov-report=html --cov-report=term-missing --junitxml=test-results.xml

# Install pre-commit hooks
pre-commit-install:
	@echo "Installing pre-commit hooks..."
	pre-commit install

# Run pre-commit on all files
pre-commit:
	@echo "Running pre-commit on all files..."
	pre-commit run --all-files 