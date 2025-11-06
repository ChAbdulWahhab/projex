<p>
  <h1>Projex</h1>
  <img src="https://i.imgur.com/Mcm57CN.png" alt="Projex Logo" width="90"/>
</p>

A powerful CLI tool to generate production-ready Python project boilerplates instantly. Skip the boring setup and jump straight into coding!

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/projex.svg)](https://badge.fury.io/py/projex)

## ✨ Features

* 🚀 **Quick Setup** - Generate complete project structures in seconds
* 🎯 **8 Framework Templates** - FastAPI, Django, Flask, Bottle, Pyramid, Tornado, Sanic, CherryPy
* 📦 **Batteries Included** - Pre-configured with best practices
* 🐳 **Docker Ready** - Includes Dockerfile and docker-compose
* ✅ **Testing Setup** - pytest configuration out of the box
* 🔧 **Smart Scaffolding** - Add models, endpoints, services, middleware with one command
* 🔐 **4 Authentication Methods** - JWT, OAuth2, API Key, Basic Auth
* 🗄️ **5 Database Options** - PostgreSQL, MySQL, MongoDB, SQLite, Redis
* 🎨 **3 Template Styles** - Minimal, Standard, Full
* 🎭 **Beautiful CLI** - Rich terminal output with progress indicators
* 🔄 **CI/CD Ready** - GitHub Actions, GitLab CI, CircleCI configs
* 📚 **Documentation Tools** - MkDocs and Sphinx setup
* 🧪 **Enhanced Testing** - Advanced pytest configs, fixtures, factories
* 🔍 **Project Validation** - Validate structure and dependencies
* 📊 **Dependency Management** - Check outdated packages, security audits
* 🌍 **Environment Management** - Multiple environment configurations
* 📝 **Makefile Generator** - Common development tasks automated
* ⚖️ **License Selection** - MIT, Apache, GPL, BSD, Unlicense
* 🙈 **Smart .gitignore** - Custom gitignore templates via gitignore.io

## 📋 Framework Templates

### FastAPI ⚡
**Modern, fast API framework with automatic documentation**

Features:
* ✅ Async/await support
* ✅ Automatic API docs (Swagger UI)
* ✅ Pydantic models for validation
* ✅ SQLAlchemy ORM integration
* ✅ Alembic migrations
* ✅ JWT authentication ready
* ✅ Docker support

**Perfect for:** RESTful APIs, WebSocket apps, high-performance services

```bash
projex create my-api --template fastapi
```

---

### Django 🎯
**Batteries-included web framework for perfectionists**

Features:
* ✅ Django REST Framework
* ✅ Admin panel out of the box
* ✅ ORM with migrations
* ✅ Custom user model ready
* ✅ CORS headers configured
* ✅ Environment variables
* ✅ pytest-django setup

**Perfect for:** Web applications, admin dashboards, CMS platforms

```bash
projex create my-site --template django
```

---

### Flask 🌶️
**Lightweight and flexible web framework**

Features:
* ✅ Flask-RESTful
* ✅ Flask-SQLAlchemy
* ✅ Flask-Migrate
* ✅ JWT authentication
* ✅ CORS support
* ✅ Blueprints structure
* ✅ Config management

**Perfect for:** Simple APIs, prototypes, custom architectures

```bash
projex create my-app --template flask
```

---

### Bottle 🍾
**Micro web framework - simple and fast**

Features:
* ✅ Single file framework
* ✅ No dependencies (except standard library)
* ✅ Built-in template engine
* ✅ Simple routing
* ✅ Fast and lightweight
* ✅ WSGI compliant
* ✅ Easy to learn

**Perfect for:** Small APIs, microservices, learning projects

```bash
projex create my-service --template bottle
```

---

### Pyramid 🔺
**Flexible, scalable web framework**

Features:
* ✅ URL generation
* ✅ Flexible authentication/authorization
* ✅ Extensible configuration
* ✅ SQLAlchemy integration
* ✅ Traversal and URL dispatch
* ✅ Built-in internationalization
* ✅ Highly modular

**Perfect for:** Large applications, complex routing, enterprise apps

```bash
projex create my-app --template pyramid
```

---

### Tornado 🌪️
**Async web framework and networking library**

Features:
* ✅ Non-blocking network I/O
* ✅ WebSocket support
* ✅ High performance
* ✅ Asynchronous handlers
* ✅ Built-in authentication
* ✅ Template engine
* ✅ Long polling support

**Perfect for:** Real-time apps, WebSocket servers, long-polling services

```bash
projex create my-realtime --template tornado
```

---

### Sanic 🚀
**Fast async framework built on uvloop**

Features:
* ✅ Blazing fast performance
* ✅ Async/await syntax
* ✅ Simple routing
* ✅ Class-based views
* ✅ Blueprint support
* ✅ Middleware support
* ✅ WebSocket support

**Perfect for:** High-performance APIs, async services, real-time apps

```bash
projex create my-fast-api --template sanic
```

---

### CherryPy 🍒
**Minimalist Python web framework**

Features:
* ✅ HTTP/1.1-compliant WSGI server
* ✅ Simple object-oriented approach
* ✅ Built-in tools (sessions, auth, caching)
* ✅ Thread-pooled web server
* ✅ Plugin system
* ✅ Configuration system
* ✅ Mature and stable

**Perfect for:** Embedded applications, traditional web apps, simple services

```bash
projex create my-server --template cherrypy
```

---

All templates include:
* ✅ Docker and docker-compose setup
* ✅ Database integration ready
* ✅ Testing setup with pytest
* ✅ Environment configuration (.env)
* ✅ CORS support configured
* ✅ Best practices structure
* ✅ README with documentation
* ✅ .gitignore configured

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

## 💻 Quick Usage

### Interactive Mode (Easiest!)

```bash
projex create
```

The CLI will guide you through:
* Project name
* Framework selection
* Database choice
* Authentication method
* Template style
* Additional options

### Command Line Mode

```bash
# Simple FastAPI project
projex create my-api --template fastapi

# Complete production-ready setup
projex create my-api \
  --template fastapi \
  --db postgresql \
  --auth jwt \
  --style full \
  --license mit

# Django with MongoDB
projex create my-site \
  --template django \
  --db mongodb \
  --author "Your Name"

# Minimal Flask app
projex create my-app \
  --template flask \
  --style minimal \
  --no-git
```

### All Create Options

```bash
projex create [PROJECT_NAME] [OPTIONS]

Options:
  -t, --template TEXT       Framework template
                            [fastapi|django|flask|bottle|pyramid|tornado|sanic|cherrypy]
  -p, --path PATH          Directory path (default: current directory)
  -a, --author TEXT        Author name
  -d, --description TEXT   Project description
  --db TEXT                Database type
                           [postgresql|mysql|mongodb|sqlite|redis]
  --style TEXT             Template style
                           [minimal|standard|full]
  --auth TEXT              Authentication method
                           [jwt|oauth2|apikey|basic]
  --license TEXT           License type
                           [mit|apache|gpl|bsd|unlicense]
  --gitignore TEXT         Gitignore templates (comma-separated)
                           Example: python,venv,pycharm,vscode
  --no-git                 Skip git initialization
  --no-venv                Skip virtual environment creation
  --help                   Show help message
```

### List Available Templates

```bash
projex list

# Output shows all 8 frameworks with descriptions
```

## 🛠️ Smart Scaffolding

Add components to your existing project:

### Add Models

```bash
# Simple model
projex add model User --fields name:str,email:str,age:int

# Complex model with multiple field types
projex add model Product --fields name:str,price:float,stock:int,is_active:bool,created_at:datetime

# Supported field types:
# str, int, float, bool, date, datetime, list, dict
```

### Add Endpoints

```bash
# CRUD endpoints
projex add endpoint users --crud

# Generates: GET, POST, PUT, DELETE endpoints
```

### Add Services

```bash
# Synchronous service
projex add service payment

# Asynchronous service
projex add service email --async
```

### Add Middleware

```bash
# CORS middleware
projex add middleware cors

# Authentication middleware
projex add middleware auth
```

**Note:** All `projex add` commands automatically detect your framework and generate appropriate code!

## 🔐 Authentication Options

### JWT (JSON Web Tokens)

```bash
projex create my-api --template fastapi --auth jwt
```

**Includes:**
* Login/register endpoints
* Password hashing with bcrypt
* Token generation and validation
* Protected route examples
* Refresh token support (optional)

### OAuth2 (Social Login)

```bash
projex create my-api --template fastapi --auth oauth2
```

**Includes:**
* Google OAuth2 integration
* GitHub OAuth2 integration
* User profile endpoints
* Token management
* Environment variable configuration

### API Key

```bash
projex create my-api --template fastapi --auth apikey
```

**Includes:**
* API key generation
* Header-based authentication
* Key rotation support
* Rate limiting ready

### Basic Authentication

```bash
projex create my-api --template flask --auth basic
```

**Includes:**
* Username/password authentication
* Base64 encoding
* Simple and straightforward
* Good for internal APIs

## 🗄️ Database Options

### PostgreSQL (Recommended for production)

```bash
projex create my-api --template fastapi --db postgresql
```

**Includes:**
* SQLAlchemy ORM configuration
* Alembic migrations
* Connection pooling
* docker-compose with PostgreSQL service
* Environment variables for connection

### MySQL/MariaDB

```bash
projex create my-api --template django --db mysql
```

**Includes:**
* MySQL-specific SQLAlchemy config
* Docker setup with MySQL
* Character set configuration

### MongoDB

```bash
projex create my-api --template fastapi --db mongodb
```

**Includes:**
* Motor (async) for FastAPI
* PyMongo for sync frameworks
* Document models
* Connection string configuration
* docker-compose with MongoDB

### SQLite (Good for development)

```bash
projex create my-api --template flask --db sqlite
```

**Includes:**
* Zero configuration needed
* File-based database
* Perfect for development/testing
* Easy to version control (optional)

### Redis

```bash
projex create my-api --template fastapi --db redis
```

**Includes:**
* redis-py configuration
* Caching examples
* Session storage setup
* docker-compose with Redis

## 🎨 Template Styles

### Minimal (Bare Bones)

```bash
projex create my-api --template fastapi --style minimal
```

**Includes:**
* Basic project structure
* Essential files only
* No Docker
* Simple configuration
* Perfect for learning

### Standard (Default, Recommended)

```bash
projex create my-api --template fastapi --style standard
# or
projex create my-api --template fastapi
```

**Includes:**
* Complete project structure
* Docker and docker-compose
* Testing setup
* Environment configuration
* Production-ready

### Full (Everything Included)

```bash
projex create my-api --template fastapi --style full
```

**Includes:**
* Everything from Standard
* CI/CD configuration
* Documentation setup
* Enhanced testing
* Code quality tools
* Makefile
* Multiple environments
* Maximum batteries included!

## 🔄 CI/CD Pipeline Generation

Generate CI/CD configurations:

### GitHub Actions

```bash
cd my-project
projex add cicd --provider github
```

**Generates:** `.github/workflows/ci.yml`

**Includes:**
* Test job (pytest)
* Lint job (black, flake8)
* Build job (Docker)
* Deploy job (commented, ready to customize)

### GitLab CI

```bash
projex add cicd --provider gitlab
```

**Generates:** `.gitlab-ci.yml`

**Includes:**
* Test stage
* Build stage
* Deploy stage
* Docker image building

### CircleCI

```bash
projex add cicd --provider circle
```

**Generates:** `.circleci/config.yml`

**Includes:**
* Workflows
* Jobs (test, build, deploy)
* Orbs integration

## 🌍 Environment Management

Manage multiple environments:

```bash
cd my-project

# Create environment files
projex env add development
projex env add staging
projex env add production
projex env add test

# List all environments
projex env list

# Show environment variables (sensitive values masked)
projex env show .env.development
projex env show .env.production
```

**Each environment file includes:**
* Database URL
* Secret keys (auto-generated)
* Debug settings
* Environment-specific configs

## 📊 Dependency Management

Manage project dependencies:

### Check Outdated Packages

```bash
cd my-project
projex deps check

# Shows:
# - Current version
# - Latest version
# - Update recommendation
```

### Update Packages

```bash
# Interactive update (prompts for each package)
projex deps update

# Update specific package
projex deps update --package fastapi

# Update all (auto-confirm)
projex deps update --all
```

### Security Audit

```bash
projex deps audit

# Uses pip-audit to check for vulnerabilities
# Shows CVE details and recommendations
```

## 📚 Documentation Setup

Add documentation to your project:

### MkDocs (Recommended)

```bash
cd my-project
projex add docs --tool mkdocs
```

**Generates:**
* `docs/` directory with structure
* `mkdocs.yml` configuration
* Material theme setup
* API documentation template
* Getting started guide

**Usage:**
```bash
mkdocs serve    # Start local server
mkdocs build    # Build static site
mkdocs gh-deploy # Deploy to GitHub Pages
```

### Sphinx

```bash
projex add docs --tool sphinx
```

**Generates:**
* `docs/` directory
* Sphinx configuration
* ReadTheDocs theme
* API autodoc setup

**Usage:**
```bash
cd docs
make html       # Build HTML docs
make clean      # Clean build files
```

## 🧪 Enhanced Testing

Add advanced testing configuration:

```bash
cd my-project
projex add test-config --enhanced
```

**Adds:**
* **pytest.ini** - Advanced pytest configuration
* **conftest.py** - Common fixtures
* **Test factories** - Factory pattern for test data
* **Coverage config** - .coveragerc file
* **Test markers** - unit, integration, slow markers
* **Example tests** - Best practices examples

**Test markers usage:**
```bash
pytest -m unit          # Run only unit tests
pytest -m integration   # Run only integration tests
pytest -m "not slow"    # Skip slow tests
pytest --cov=app        # Run with coverage
```

## 📝 Makefile Generator

Add common development tasks:

```bash
cd my-project
projex add makefile
```

**Generated targets:**
```makefile
make install      # Install dependencies
make test         # Run tests
make test-cov     # Run tests with coverage
make run          # Start development server
make docker-build # Build Docker image
make docker-up    # Start Docker containers
make docker-down  # Stop Docker containers
make clean        # Clean cache files
make lint         # Run linters
make format       # Format code
make migrate      # Run database migrations (Django/Flask)
make help         # Show all commands
```

**Framework-aware:** Commands adapt to your framework!

## 🔧 Code Quality Tools

Add pre-commit hooks and linting:

```bash
cd my-project
projex add quality-tools
```

**Adds:**
* **.pre-commit-config.yaml** - Pre-commit hooks
* **pyproject.toml** - Tool configurations
* **black** - Code formatting
* **isort** - Import sorting
* **flake8** - Linting
* **mypy** - Type checking
* **pylint** - Advanced linting

**Setup:**
```bash
pip install -r requirements-dev.txt
pre-commit install
pre-commit run --all-files  # Run manually
```

## 🔍 Project Validation

Validate your project structure:

```bash
cd my-project
projex validate
# or
projex doctor

# Checks:
# ✓ Required files exist
# ✓ Project structure is correct
# ✓ Dependencies are valid
# ✓ No import errors
# ✓ Docker files are configured
# ✓ Tests are runnable
```

## 📊 Project Information

Get detailed project stats:

```bash
cd my-project
projex info

# Shows:
# - Project name and template
# - Python version
# - Total files and lines of code
# - Dependencies count
# - Last modified date
# - Git status
# - Docker configuration
# - Test count
# - Coverage percentage
```

## ⚖️ License Selection

Add license during creation:

```bash
# MIT License (permissive)
projex create my-api --template fastapi --license mit

# Apache 2.0 (with patent grant)
projex create my-api --template django --license apache

# GPL v3 (copyleft)
projex create my-api --template flask --license gpl

# BSD 3-Clause
projex create my-api --template bottle --license bsd

# Unlicense (public domain)
projex create my-api --template pyramid --license unlicense
```

## 🙈 Smart .gitignore

Generate custom .gitignore:

```bash
# Multiple templates
projex create my-api \
  --template fastapi \
  --gitignore python,venv,pycharm,vscode,macos

# Uses gitignore.io API to fetch latest templates
```

**Popular templates:**
* `python` - Python-specific
* `venv` - Virtual environments
* `pycharm` - PyCharm IDE
* `vscode` - VS Code
* `visualstudio` - Visual Studio
* `macos` - macOS files
* `windows` - Windows files
* `linux` - Linux files
* `node` - Node.js (if using frontend)

## 📁 Project Structure Examples

### FastAPI (Standard)

```
my-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── api/
│   │   └── v1/
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── users.py
│   │           └── items.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   └── services/
│       └── __init__.py
├── tests/
│   ├── conftest.py
│   ├── test_main.py
│   └── api/
│       └── test_users.py
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml (if quality-tools added)
├── Dockerfile
├── docker-compose.yml
├── Makefile (if generated)
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

### Django (Standard)

```
my-site/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── __init__.py
│   └── core/
│       ├── __init__.py
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── admin.py
│       ├── serializers.py
│       └── tests.py
├── static/
├── media/
├── templates/
├── manage.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
└── README.md
```

### Flask (Standard)

```
my-app/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/
│   │   └── __init__.py
│   └── services/
│       └── __init__.py
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── migrations/
├── run.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🎯 Real-World Usage Examples

### Production API

```bash
projex create production-api \
  --template fastapi \
  --db postgresql \
  --auth jwt \
  --style full \
  --license mit \
  --gitignore python,venv,pycharm,vscode

cd production-api
projex add cicd --provider github
projex add docs --tool mkdocs
projex add quality-tools
projex env add staging
projex env add production
```

### Microservices

```bash
# User Service
projex create user-service --template fastapi --db postgresql

# Order Service
projex create order-service --template fastapi --db postgresql

# Payment Service
projex create payment-service --template fastapi --db redis
```

### Monolith Application

```bash
projex create my-app \
  --template django \
  --db mysql \
  --auth oauth2 \
  --style full

cd my-app
projex add cicd --provider gitlab
projex add docs --tool sphinx
```

## 🐳 Docker Usage

### Development

```bash
cd my-project
docker-compose up
```

### Production Build

```bash
docker build -t my-app:latest .
docker run -p 8000:8000 --env-file .env.production my-app:latest
```

### With Database

```bash
# docker-compose automatically starts database service
docker-compose up

# Your app connects to database automatically via DATABASE_URL
```

## ✅ Testing

### Run Tests

```bash
cd my-project
source venv/bin/activate

# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Open coverage report
open htmlcov/index.html
```

### Test Markers (if enhanced testing added)

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/ChAbdulWahhab/projex.git
cd projex

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in editable mode
pip install -e .
pip install -r requirements-dev.txt

# Run tests
pytest

# Install pre-commit hooks
pre-commit install
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

* Built with [Click](https://click.palletsprojects.com/) for CLI
* [Rich](https://github.com/Textualize/rich) for beautiful terminal output
* [Jinja2](https://jinja.palletsprojects.com/) for templating
* Framework logos and inspiration from respective communities

## 📮 Support

* 📧 **Email:** ch.abdul.wahhab@proton.me
* 💬 **Discussions:** [GitHub Discussions](https://github.com/ChAbdulWahhab/projex/discussions)
* 🐛 **Bug Reports:** [GitHub Issues](https://github.com/ChAbdulWahhab/projex/issues)
* 📖 **Documentation:** [Full Docs](https://chabdulwahhab.github.io/projex/)

## 🗺️ Roadmap

### Completed ✅
* [x] 8 Framework templates
* [x] 5 Database options
* [x] 4 Authentication methods
* [x] 3 Template styles
* [x] Smart scaffolding system
* [x] CI/CD pipeline generation
* [x] Environment management
* [x] Dependency management
* [x] Documentation setup
* [x] Enhanced testing
* [x] Code quality tools
* [x] Project validation
* [x] License selection
* [x] Smart gitignore

### Upcoming 🚀
* [ ] Frontend templates (React, Vue, Svelte)
* [ ] GraphQL templates
* [ ] Kubernetes deployment files
* [ ] Terraform configurations
* [ ] API Gateway templates
* [ ] Message queue integration (RabbitMQ, Kafka)
* [ ] Monitoring setup (Prometheus, Grafana)
* [ ] Plugin system
* [ ] Template marketplace

## 📊 Project Stats

* **Templates:** 8 frameworks
* **Databases:** 5 options
* **Auth Methods:** 4 types
* **CI/CD Providers:** 3 platforms
* **Commands:** 15+ commands
* **Active Users:** Growing daily!
* **GitHub Stars:** ⭐ Give us a star!

## 🌟 Show Your Support

If you find Projex helpful, please consider:
* ⭐ Starring the repository
* 🐦 Sharing on social media
* 📝 Writing a blog post
* 🤝 Contributing code
* 💬 Joining discussions

---

**Made with ❤️ by Ch. Abdul Wahab**

**Project Link:** [https://github.com/ChAbdulWahhab/projex](https://github.com/ChAbdulWahhab/projex)
<br>
**PyPi Link:** [https://pypi.org/project/projex-cli/](https://pypi.org/project/projex-cli/)

Happy coding! 🚀