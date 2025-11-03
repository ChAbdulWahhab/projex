# 🔨 Projex

A powerful CLI tool to generate production-ready Python project boilerplates instantly. Skip the boring setup and jump straight into coding!

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

* 🚀 **Quick Setup** - Generate complete project structures in seconds
* 🎯 **Multiple Templates** - FastAPI, Django, and Flask templates
* 📦 **Batteries Included** - Pre-configured with best practices
* 🐳 **Docker Ready** - Includes Dockerfile and docker-compose
* ✅ **Testing Setup** - pytest configuration out of the box
* 🔧 **Customizable** - Easy to modify and extend
* 🎨 **Beautiful CLI** - Rich terminal output with progress indicators

## 📋 Available Templates

### FastAPI

Modern, fast API framework with automatic documentation

* ✅ Async/await support
* ✅ Automatic API docs (Swagger UI)
* ✅ Pydantic models for validation
* ✅ SQLAlchemy ORM integration
* ✅ Alembic migrations
* ✅ JWT authentication ready
* ✅ Docker support

### Django

Batteries-included web framework for perfectionists

* ✅ Django REST Framework
* ✅ Admin panel
* ✅ ORM with migrations
* ✅ Custom user model ready
* ✅ CORS headers configured
* ✅ Environment variables
* ✅ pytest-django setup

### Flask

Lightweight and flexible web framework

* ✅ Flask-RESTful
* ✅ Flask-SQLAlchemy
* ✅ Flask-Migrate
* ✅ JWT authentication
* ✅ CORS support
* ✅ Blueprints structure
* ✅ Config management

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
  -t, --template [fastapi|django|flask]  Project template type
  -p, --path PATH                        Directory path (default: current)
  -a, --author TEXT                      Author name
  -d, --description TEXT                 Project description
  --no-git                               Skip git initialization
  --no-venv                              Skip virtual environment creation
  --help                                 Show help message
```

### List Available Templates

```bash
projex list
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

## 🗺️ Roadmap

* [ ] Add React/Next.js frontend templates
* [ ] Add GraphQL templates
* [ ] Add microservices architecture templates
* [ ] Add CI/CD pipeline configurations
* [ ] Add Kubernetes deployment files
* [ ] Interactive template customization
* [ ] Plugin system for custom templates
* [ ] Project template marketplace

---

Made with ❤️ by developers, for developers