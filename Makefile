.PHONY: help install install-dev run test format lint clean docker-build docker-run docker-stop

# Default target
help:
	@echo "Available commands:"
	@echo "  help         - Show this help message"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  run          - Run the application in development mode"
	@echo "  test         - Run tests"
	@echo "  format       - Format code with black and isort"
	@echo "  lint         - Run linting with flake8 and mypy"
	@echo "  clean        - Clean up cache files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run with Docker Compose"
	@echo "  docker-stop  - Stop Docker Compose services"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

# Development
run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Testing
test:
	pytest tests/ -v --cov=app --cov-report=html

# Code quality
format:
	black app/
	isort app/

lint:
	flake8 app/
	mypy app/

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

# Docker
docker-build:
	docker build -t organization-api .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

# Environment setup
setup-env:
	cp .env.example .env
	@echo "Please edit .env file with your configuration"

# Database
db-reset:
	@echo "This will drop all collections in the database"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		python -c "from app.core.database import connect_to_mongo, get_database; import asyncio; async def reset(): await connect_to_mongo(); db = get_database(); collections = await db.list_collection_names(); [await db.drop_collection(c) for c in collections]; print('Database reset complete'); asyncio.run(reset())"; \
	fi 