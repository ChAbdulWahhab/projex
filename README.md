# 🔨 Projex

A powerful CLI tool to generate production-ready Python project boilerplates instantly. Skip the boring setup and jump straight into coding!

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

* 🚀 **Quick Setup** - Generate complete project structures in seconds
* 🎯 **8 Framework Templates** - FastAPI, Django, Flask, Bottle, Pyramid, Tornado, Sanic, CherryPy
* 📦 **Batteries Included** - Pre-configured with best practices
* 🐳 **Docker Ready** - Includes Dockerfile and docker-compose
* ✅ **Testing Setup** - pytest configuration out of the box
* 🔧 **Smart Scaffolding** - Add models, endpoints, services, middleware with one command
* 🔐 **Authentication Options** - JWT, OAuth2, API Key, Basic Auth
* 🗄️ **Multiple Databases** - PostgreSQL, MySQL, MongoDB, SQLite, Redis
* 🎨 **Beautiful CLI** - Rich terminal output with progress indicators
* 🔄 **CI/CD Ready** - Generate GitHub Actions, GitLab CI, CircleCI configs
* 📚 **Documentation** - MkDocs and Sphinx setup
* 🧪 **Enhanced Testing** - Advanced pytest configs, fixtures, factories
* 🔍 **Project Validation** - Validate project structure and dependencies
* 📊 **Dependency Management** - Check outdated packages, security audits
* 🌍 **Environment Management** - Multiple environment configurations
* 📝 **Makefile Generator** - Common development tasks

## 📋 Available Templates

### FastAPI
Modern, fast API framework with automatic documentation

### Django
Batteries-included web framework for perfectionists

### Flask
Lightweight and flexible web framework

### Bottle
Micro web framework - simple and fast

### Pyramid
Flexible, scalable web framework

### Tornado
Async web framework and networking library

### Sanic
Fast async framework built on uvloop

### CherryPy
Minimalist Python web framework

All templates include:
* ✅ Docker support
* ✅ Database integration
* ✅ Testing setup (pytest)
* ✅ Environment configuration
* ✅ CORS support
* ✅ Best practices structure

## 🚀 Installation

### From PyPI (recommended)

```bash
pip install projex
```

### From Source

```bash
git clone https://github.com/ChAbdulWahhab/projex.git
cd projex
pip install -e .
```

## 💻 Usage

### Interactive Mode (Recommended)

```bash
projex create
```

The CLI will guide you through the project creation process with interactive prompts.

### Quick Start with Arguments

```bash
# Create a FastAPI project
projex create my-api --template fastapi --author "Your Name"

# Create a Django project
projex create my-site --template django --description "My awesome site"

# Create a Flask project
projex create my-app --template flask
```

### Command Options

```bash
projex create [PROJECT_NAME] [OPTIONS]

Options:
  -t, --template TEMPLATE    Framework template (fastapi, django, flask, etc.)
  -p, --path PATH            Directory path (default: current)
  -a, --author TEXT          Author name
  -d, --description TEXT     Project description
  --db DATABASE              Database type (postgresql, mysql, mongodb, sqlite, redis)
  --style STYLE              Template style (minimal, standard, full)
  --auth AUTH                Authentication (jwt, oauth2, apikey, basic)
  --license LICENSE          License type (mit, apache, gpl, bsd, unlicense)
  --gitignore TEMPLATES      Gitignore templates (python,venv,pycharm, etc.)
  --no-git                   Skip git initialization
  --no-venv                  Skip virtual environment creation
```

### List Available Templates

```bash
projex list
```

## 🛠️ Advanced Commands

### Smart Scaffolding

Add components to your project:

```bash
# Add a model
projex add model User --fields name:str,email:str,age:int

# Add CRUD endpoints
projex add endpoint users --crud

# Add a service
projex add service email --async

# Add middleware
projex add middleware cors
```

### CI/CD Pipeline Generation

```bash
# GitHub Actions
projex add cicd --provider github

# GitLab CI
projex add cicd --provider gitlab

# CircleCI
projex add cicd --provider circle
```

### Environment Management

```bash
# Add environment files
projex env add development
projex env add staging
projex env add production

# List environment files
projex env list

# Show environment variables
projex env show .env.development
```

### Dependency Management

```bash
# Check outdated packages
projex deps check

# Update packages
projex deps update

# Security audit
projex deps audit
```

### Documentation Setup

```bash
# MkDocs (default)
projex add docs --tool mkdocs

# Sphinx
projex add docs --tool sphinx
```

### Testing Enhancements

```bash
# Enhanced test configuration
projex add test-config --enhanced
```

### Additional Tools

```bash
# Generate Makefile
projex add makefile

# Add quality tools (black, isort, flake8, mypy)
projex add quality-tools

# Validate project
projex validate

# Show project info
projex info
```

## 📁 Generated Project Structure

### FastAPI

```
my-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── api/
│   │   └── v1/
│   │       ├── router.py
│   │       └── endpoints/
│   ├── models/
│   └── schemas/
├── tests/
│   └── test_main.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

### Django

```
my-site/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   └── core/
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       └── tests.py
├── manage.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

### Flask

```
my-app/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   └── models/
├── tests/
│   └── test_api.py
├── run.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🎯 Quick Start After Generation

### FastAPI

```bash
cd my-api
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# Visit http://localhost:8000/docs for API documentation
```

### Django

```bash
cd my-site
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# Visit http://localhost:8000/admin
```

### Flask

```bash
cd my-app
source venv/bin/activate
pip install -r requirements.txt
python run.py
# Visit http://localhost:5000
```

## 🐳 Docker Support

All templates come with Docker support:

```bash
# Build and run with docker-compose
docker-compose up --build

# Or use Docker directly
docker build -t my-project .
docker run -p 8000:8000 my-project
```

## ✅ Testing

All projects include pytest configuration:

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## 🔧 Customization

### Adding Custom Templates

You can extend Projex by adding your own templates:

1. Create a new template configuration in `config.py`
2. Add template generation logic in `generator.py`
3. Update the CLI to include your template

### Modifying Existing Templates

Edit the template generation methods in `generator.py`:

* `_generate_fastapi()`
* `_generate_django()`
* `_generate_flask()`

## 📝 Environment Variables

All generated projects use `.env` files for configuration. Copy `.env.example` to `.env` and update with your values:

```bash
cp .env.example .env
```

Common variables:

* `DATABASE_URL` - Database connection string
* `SECRET_KEY` - Application secret key
* `DEBUG` - Debug mode (True/False)
* `ENVIRONMENT` - Environment name (development/production)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/ChAbdulWahhab/projex.git
cd projex

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e .
pip install -r requirements-dev.txt

# Run tests
pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

* Built with [Click](https://click.palletsprojects.com/) for CLI
* [Rich](https://github.com/Textualize/rich) for beautiful terminal output
* [Jinja2](https://jinja.palletsprojects.com/) for templating

## 📮 Contact

**Ch Abdul Wahhab**
Project Link: [https://github.com/ChAbdulWahhab/projex](https://github.com/ChAbdulWahhab/projex)

## 🎯 Use Cases

### Microservices Architecture
```bash
projex create user-service --template fastapi
projex create order-service --template fastapi
projex create payment-service --template fastapi
```

### Full-Stack Application
```bash
# Backend API
projex create backend --template fastapi --db postgresql --auth jwt

# Admin Dashboard
projex create admin --template django
```

### Production-Ready API
```bash
projex create my-api --template fastapi \
  --db postgresql \
  --auth jwt \
  --style full \
  --license mit

cd my-api
projex add cicd --provider github
projex add docs --tool mkdocs
projex add quality-tools
projex env add production
```

## 🗺️ Roadmap

* [x] Multiple framework templates (8 frameworks)
* [x] Database selection (5 databases)
* [x] Authentication options
* [x] CI/CD pipeline generation
* [x] Environment management
* [x] Dependency management
* [x] Documentation setup
* [x] Smart scaffolding system
* [x] Project validation
* [ ] Add React/Next.js frontend templates
* [ ] Add GraphQL templates
* [ ] Add Kubernetes deployment files
* [ ] Interactive template customization
* [ ] Plugin system for custom templates

---

Made with ❤️ by developers, for developers