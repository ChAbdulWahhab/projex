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