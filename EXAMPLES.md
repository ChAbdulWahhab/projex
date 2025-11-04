# 📚 Usage Examples

Comprehensive examples of using **Projex** in different scenarios.

## Table of Contents

* [Basic Usage](#basic-usage)
* [Advanced Usage](#advanced-usage)
* [Real-World Scenarios](#real-world-scenarios)
* [Template Customization](#template-customization)

---

## Basic Usage

### Creating Your First API

```bash
# Interactive mode - easiest way!
projex create

# Or with all options
projex create my-first-api \
  --template fastapi \
  --author "John Doe" \
  --description "My first API project"
```

### Specifying Custom Path

```bash
# Create in specific directory
projex create my-api --template fastapi --path ~/projects

# This creates: ~/projects/my-api/
```

### Skip Optional Steps

```bash
# Skip git initialization
projex create my-api --template django --no-git

# Skip virtual environment creation
projex create my-api --template flask --no-venv

# Skip both
projex create my-api --template fastapi --no-git --no-venv
```

---

## Advanced Usage

### Microservices Architecture

Create multiple services:

```bash
# User service
projex create user-service --template fastapi --path services/

# Order service
projex create order-service --template fastapi --path services/

# Payment service
projex create payment-service --template fastapi --path services/

# API Gateway
projex create api-gateway --template flask --path services/
```

Result:

```
services/
├── user-service/
├── order-service/
├── payment-service/
└── api-gateway/
```

---

### Full-Stack Application

```bash
# Backend API
projex create backend --template fastapi

# Admin Dashboard
projex create admin --template django

# Result:
# backend/   - FastAPI for mobile/web API
# admin/     - Django admin panel
```

---

### Team Project Setup

```bash
# Create project for team
projex create team-project \
  --template django \
  --author "Development Team" \
  --description "Team collaboration platform"

cd team-project

# Commit and push
git remote add origin https://github.com/team/project.git
git push -u origin main
```

---

## Real-World Scenarios

### E-Commerce Backend

```bash
# Create FastAPI project
projex create ecommerce-api --template fastapi

cd ecommerce-api

# Project structure ready!
# Add your models, endpoints, and business logic
```

Example endpoint:

```python
# app/api/v1/endpoints/products.py
from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter()

@router.get("/products")
async def get_products():
    return {"products": []}

@router.post("/products")
async def create_product(product: dict):
    return {"id": 1}
```

---

### Blog Platform

```bash
# Create Django project
projex create my-blog --template django

cd my-blog
source venv/bin/activate
pip install -r requirements.txt

# Create blog app
python manage.py startapp blog

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

---

### REST API for Mobile App

```bash
# FastAPI for high performance
projex create mobile-api --template fastapi

# Key features included:
# ✓ JWT authentication
# ✓ CORS configured
# ✓ Database ORM
# ✓ Async support
# ✓ API documentation
```

---

### Data Processing Service

```bash
# Flask for flexibility
projex create data-processor --template flask

cd data-processor
```

---

### Webhook Handler

```bash
projex create webhook-handler --template fastapi

cd webhook-handler
```

Webhook example:

```python
# app/api/v1/endpoints/webhooks.py
@router.post("/webhook")
async def handle_webhook(payload: dict):
    return {"status": "received"}
```

---

## Template Customization

### Custom Development Workflow

```bash
projex create my-project --template fastapi --no-venv

cd my-project

conda create -n myproject python=3.11
conda activate myproject
pip install -r requirements.txt
```

---

### With Custom Database

```bash
projex create my-api --template django

cd my-api

echo "DATABASE_URL=postgresql://user:pass@localhost:5432/mydb" > .env
python manage.py migrate
```

---

### Docker-First Development

```bash
projex create my-service --template fastapi

cd my-service
docker-compose up --build
```

---

### Testing-First Approach

```bash
projex create tdd-project --template flask

cd tdd-project
source venv/bin/activate
pip install -r requirements-dev.txt

pytest --cov=app tests/
```

---

## Template Comparison

### When to Use FastAPI

```bash
projex create my-api --template fastapi
```

**Best For:**

* RESTful APIs
* Async processing
* WebSocket apps
* Background tasks
* High concurrency

---

### When to Use Django

```bash
projex create my-site --template django
```

**Best For:**

* Web apps
* Admin dashboards
* CMS platforms
* E-commerce sites

---

### When to Use Flask

```bash
projex create my-app --template flask
```

**Best For:**

* Simple APIs
* Prototypes
* Custom architectures
* Learning projects

---

## Automation Scripts

### Batch Project Creation

```bash
#!/bin/bash
# create-services.sh

services=("auth" "users" "products" "orders")

for service in "${services[@]}"; do
  projex create "${service}-service" \
    --template fastapi \
    --path microservices/ \
    --no-venv
done
```

---

### CI/CD Integration

```yaml
# .github/workflows/deploy.yml
- name: Setup project
  run: |
    pip install projex
    projex create deployment-test --template fastapi --no-git --no-venv
```

---

## Pro Tips

### Quick API Testing

```bash
projex create test-api --template fastapi --no-git
cd test-api
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload &
curl http://localhost:8000/health
```

---

### Multiple Environments

```bash
projex create my-api-dev --template fastapi
projex create my-api-staging --template fastapi
```

---

### Template Learning

```bash
projex create learn-fastapi --template fastapi --no-venv
projex create learn-django --template django --no-venv
projex create learn-flask --template flask --no-venv
```

---

### Rapid Prototyping

```bash
projex create prototype --template flask --no-git --no-venv
cd prototype
python run.py
```

---

## Common Patterns

### API + Frontend

```bash
projex create api --template fastapi
projex create admin --template django
```

---

### Monorepo Setup

```bash
mkdir my-project && cd my-project
projex create api --template fastapi --no-git
projex create admin --template django --no-git
git init
git add .
git commit -m "Initial commit"
```

---

## Advanced Workflows

### Complete Production Setup

```bash
# 1. Create project with all features
projex create my-api \
  --template fastapi \
  --db postgresql \
  --auth jwt \
  --style full \
  --license mit

cd my-api

# 2. Add CI/CD
projex add cicd --provider github

# 3. Add documentation
projex add docs --tool mkdocs

# 4. Add quality tools
projex add quality-tools

# 5. Add Makefile
projex add makefile

# 6. Create environments
projex env add development
projex env add staging
projex env add production

# 7. Add enhanced testing
projex add test-config --enhanced

# 8. Validate everything
projex validate
```

### Microservices Architecture

```bash
# Create multiple services
projex create user-service --template fastapi --path services/
projex create order-service --template fastapi --path services/
projex create payment-service --template fastapi --path services/

# Add CI/CD to each
cd services/user-service && projex add cicd --provider github
cd ../order-service && projex add cicd --provider github
cd ../payment-service && projex add cicd --provider github
```

### Adding Components to Existing Project

```bash
cd my-project

# Add models
projex add model User --fields name:str,email:str,age:int
projex add model Product --fields name:str,price:float,stock:int

# Add endpoints
projex add endpoint users --crud
projex add endpoint products --crud

# Add services
projex add service email --async
projex add service notification

# Add middleware
projex add middleware cors
projex add middleware auth
```

### Database Selection Examples

```bash
# PostgreSQL (default)
projex create my-api --template fastapi --db postgresql

# MySQL
projex create my-api --template django --db mysql

# MongoDB
projex create my-api --template fastapi --db mongodb

# SQLite (for development)
projex create my-api --template flask --db sqlite

# Redis (for caching)
projex create my-api --template fastapi --db redis
```

### Authentication Examples

```bash
# JWT Authentication
projex create my-api --template fastapi --auth jwt

# OAuth2
projex create my-api --template fastapi --auth oauth2

# API Key
projex create my-api --template fastapi --auth apikey

# Basic Auth
projex create my-api --template fastapi --auth basic
```

### Template Styles

```bash
# Minimal (bare minimum)
projex create my-api --template fastapi --style minimal

# Standard (default)
projex create my-api --template fastapi --style standard

# Full (everything included)
projex create my-api --template fastapi --style full
```

### Dependency Management

```bash
cd my-project

# Check outdated packages
projex deps check

# Update specific package
projex deps update --package fastapi

# Update all packages (interactive)
projex deps update

# Security audit
projex deps audit
```

### Environment Configuration

```bash
cd my-project

# Create environment files
projex env add development
projex env add staging
projex env add production
projex env add test

# List all environments
projex env list

# View environment variables
projex env show .env.development
projex env show .env.production
```

### Documentation Setup

```bash
cd my-project

# MkDocs (recommended for most projects)
projex add docs --tool mkdocs
mkdocs serve  # Start local server
mkdocs build  # Build static site
mkdocs gh-deploy  # Deploy to GitHub Pages

# Sphinx (for complex documentation)
projex add docs --tool sphinx
cd docs && make html
```

### Testing Workflow

```bash
cd my-project

# Add enhanced test configuration
projex add test-config --enhanced

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run only unit tests
pytest -m unit

# Skip slow tests
pytest -m "not slow"

# Run integration tests
pytest -m integration
```

### Project Validation

```bash
cd my-project

# Validate project structure
projex validate

# Show detailed project info
projex info

# Doctor command (alias for validate)
projex doctor
```

## More Examples

Check out our [Examples Repository](https://github.com/ChAbdulWahhab/projex-examples) for:

* Full app demos
* Deployment configs
* Integration patterns
* Best practices
* Real-world projects

---

## Need Help?

* 📖 [Full Documentation](README.md)
* 🚀 [Quick Start Guide](QUICKSTART.md)
* 🤝 [Contributing](CONTRIBUTING.md)
* 💬 [Discussions](https://github.com/ChAbdulWahhab/projex/discussions)