.PHONY: help test coverage clean install dev server build stop up down logs shell test-build test-clean check makemigrations migrate

# Default target
help:
	@echo "HR System Backend - Available Commands:"
	@echo ""
	@echo "Server/Development:"
	@echo "  server      - Start development server (API only)"
	@echo "  up          - Start all services (API + DB)"
	@echo "  down        - Stop all services"
	@echo "  logs        - Show logs for all services"
	@echo "  shell       - Open shell in API container"
	@echo ""
	@echo "Database:"
	@echo "  makemigrations - Create database migrations"
	@echo "  migrate       - Apply database migrations"
	@echo ""
	@echo "Testing:"
	@echo "  test        - Run all tests with coverage"
	@echo "  coverage    - Run tests with coverage report"
	@echo "  check       - Run Django system check"
	@echo "  test-build  - Build test environment"
	@echo "  test-clean  - Clean up test containers and volumes"
	@echo ""
	@echo "Development:"
	@echo "  install     - Install dependencies"
	@echo "  dev         - Install development dependencies"
	@echo "  clean       - Clean up generated files"
	@echo "  build       - Build Docker images"

# Install dependencies
install:
	@echo "Installing dependencies..."
	docker-compose -f ../compose/docker-compose.yml run --rm api pip install -e .

dev:
	@echo "Installing development dependencies..."
	docker-compose -f ../compose/docker-compose.yml run --rm api pip install -e ".[dev]"

# Build test environment
test-build:
	@echo "Building test environment..."
	docker-compose  -f ../compose/docker-compose.test.yml build

# Run Django check
check:
	@echo "Running Django check..."
	docker-compose -f ../compose/docker-compose.yml run --rm api python manage.py check

# Run all tests with coverage
test:
	@echo "Running all tests with coverage..."
	docker-compose -f ../compose/docker-compose.test.yml run --rm test

coverage:
	@echo "Running tests with coverage report..."
	docker-compose  -f ../compose/docker-compose.test.yml run --rm test
	@echo "Cleaning up test containers..."
	docker-compose  -f ../compose/docker-compose.test.yml down --remove-orphans -v

# Clean up test containers and volumes
test-clean:
	@echo "Cleaning up test containers and volumes..."
	docker-compose  -f ../compose/docker-compose.test.yml down --remove-orphans -v

# Clean up generated files
clean:
	@echo "Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov .pytest_cache
	rm -rf build dist
	@echo "Cleaning up test containers..."
	docker-compose -f ../compose/docker-compose.test.yml down -v

# Start development server (API only)
server:
	@echo "Starting development server..."
	docker-compose -f ../compose/docker-compose.yml up api

# Start all services (API + DB)
up:
	@echo "Starting all services..."
	docker-compose -f ../compose/docker-compose.yml up

# Start all services in background
up-d:
	@echo "Starting all services in background..."
	docker-compose -f ../compose/docker-compose.yml up -d

# Stop all services
down:
	@echo "Stopping all services..."
	docker-compose -f ../compose/docker-compose.yml down

# Show logs for all services
logs:
	@echo "Showing logs..."
	docker-compose -f ../compose/docker-compose.yml logs -f

# Show logs for specific service
logs-api:
	@echo "Showing API logs..."
	docker-compose -f ../compose/docker-compose.yml logs -f api

logs-celery:
	@echo "Showing Celery logs..."
	docker-compose -f ../compose/docker-compose.yml logs -f celery

# Open shell in API container
shell:
	@echo "Opening shell in API container..."
	docker-compose -f ../compose/docker-compose.yml run --rm api bash

# Open shell in Celery container
shell-celery:
	@echo "Opening shell in Celery container..."
	docker-compose -f ../compose/docker-compose.yml run --rm celery bash

# Build Docker images
build:
	@echo "Building Docker images..."
	docker-compose -f ../compose/docker-compose.yml build

# Stop all services
stop:
	@echo "Stopping all services..."
	docker-compose -f ../compose/docker-compose.yml down

# Create database migrations
makemigrations:
	@echo "Creating database migrations..."
	docker-compose -f ../compose/docker-compose.yml run --rm api python manage.py makemigrations

# Apply database migrations
migrate:
	@echo "Applying database migrations..."
	docker-compose -f ../compose/docker-compose.yml run --rm api python manage.py migrate