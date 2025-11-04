"""Makefile generation utilities"""
from pathlib import Path
from typing import Optional


def generate_makefile(project_path: Path, framework: Optional[str] = None) -> Path:
    """
    Generate Makefile with common targets.
    
    Args:
        project_path: Path to project root
        framework: Detected framework name
        
    Returns:
        Path to created Makefile
    """
    # Determine run command based on framework
    run_command = 'python app/main.py'
    migrate_command = ''
    create_superuser_command = ''
    
    if framework == 'django':
        run_command = 'python manage.py runserver'
        migrate_command = 'python manage.py migrate'
        create_superuser_command = 'python manage.py createsuperuser'
    elif framework == 'fastapi':
        run_command = 'uvicorn app.main:app --reload --host 0.0.0.0 --port 8000'
    elif framework == 'flask':
        run_command = 'python run.py'
    elif framework == 'pyramid':
        run_command = 'pserve development.ini --reload'
    elif framework == 'sanic':
        run_command = 'python -m sanic app.main.app --host 0.0.0.0 --port 8000 --dev'
    elif framework == 'tornado':
        run_command = 'python app/main.py'
    elif framework == 'bottle':
        run_command = 'python app/main.py'
    elif framework == 'cherrypy':
        run_command = 'python app/main.py'
    
    makefile_content = f""".PHONY: help install install-dev test test-cov run docker-build docker-up docker-down clean lint format migrate superuser

# Default target
help:
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make install-dev   - Install development dependencies"
	@echo "  make test          - Run tests"
	@echo "  make test-cov      - Run tests with coverage"
	@echo "  make run           - Run development server"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-up     - Start Docker containers"
	@echo "  make docker-down   - Stop Docker containers"
	@echo "  make clean         - Clean Python cache files"
	@echo "  make lint          - Run linting checks"
	@echo "  make format        - Format code with black and isort"
"""
    
    if migrate_command:
        makefile_content += """	@echo "  make migrate       - Run database migrations"
"""
    
    if create_superuser_command:
        makefile_content += """	@echo "  make superuser     - Create superuser (Django)"
"""
    
    makefile_content += f"""
# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Testing
test:
	pytest -v

test-cov:
	pytest --cov=app --cov-report=html --cov-report=term-missing

# Running
run:
	{run_command}
"""
    
    if migrate_command:
        makefile_content += f"""
# Database migrations
migrate:
	{migrate_command}
"""
    
    if create_superuser_command:
        makefile_content += f"""
# Create superuser (Django only)
superuser:
	{create_superuser_command}
"""
    
    makefile_content += """
# Docker
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Cleanup
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true

# Code quality
lint:
	black --check .
	isort --check-only .
	flake8 . || true
	mypy . || true

format:
	black .
	isort .
"""
    
    makefile_file = project_path / 'Makefile'
    makefile_file.write_text(makefile_content)
    
    return makefile_file

