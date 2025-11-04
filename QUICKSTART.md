# 🚀 Quick Start Guide

Get started with **Projex** in under 5 minutes!

## Installation

```bash
pip install projex
```

## Your First Project

### Interactive Mode (Recommended)

```bash
projex create
```

Just answer a few questions and you're done! ✨

### FastAPI Project

```bash
# Create project
projex create my-api --template fastapi

# Navigate and setup
cd my-api
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run it!
uvicorn app.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation! 📚

### Django Project

```bash
# Create project
projex create my-site --template django

# Setup
cd my-site
source venv/bin/activate
pip install -r requirements.txt

# Initialize database
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit [http://localhost:8000/admin](http://localhost:8000/admin) for admin panel! 🎨

### Flask Project

```bash
# Create project
projex create my-app --template flask

# Setup
cd my-app
source venv/bin/activate
pip install -r requirements.txt

# Run it!
python run.py
```

Visit [http://localhost:5000](http://localhost:5000) ! 🎯

## Using Docker

All projects come with Docker support:

```bash
cd your-project
docker-compose up --build
```

That's it! Your app is running in Docker! 🐳

## Next Steps

### Add Your First API Endpoint (FastAPI)

Edit `app/api/v1/endpoints/items.py`:

```python
@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello, {name}!"}
```

### Add Your First View (Django)

Edit `apps/core/views.py`:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def hello(request, name):
    return Response({'message': f'Hello, {name}!'})
```

### Add Your First Route (Flask)

Edit `app/api/routes.py`:

```python
@api_bp.route('/hello/<name>')
def say_hello(name):
    return jsonify({'message': f'Hello, {name}!'})
```

## Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

## Environment Configuration

1. Copy `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your settings:

   ```env
   DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

## Common Commands

### List Available Templates

```bash
projex list
```

### Get Help

```bash
projex --help
projex create --help
```

### Skip Git/Virtual Environment

```bash
projex create my-project --template fastapi --no-git --no-venv
```

## Tips & Tricks

💡 **Pro Tip 1**: Use `--no-venv` if you prefer using conda or other virtual env tools
💡 **Pro Tip 2**: Add `--author "Your Name"` to customize project metadata
💡 **Pro Tip 3**: Check generated README.md for project-specific instructions
💡 **Pro Tip 4**: All templates include pytest - start writing tests from day one!

## Troubleshooting

### Import Errors

```bash
# Make sure you're in virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use

```bash
# FastAPI - change port
uvicorn app.main:app --port 8001

# Django - change port
python manage.py runserver 8001

# Flask - change port
flask run --port 5001
```

### Database Connection Issues

* Check your `.env` file has correct DATABASE_URL
* Ensure database server is running
* For SQLite (default), no setup needed!

## What's Included?

Every generated project includes:

✅ Production-ready project structure
✅ Docker configuration
✅ Environment variable management
✅ Testing setup with pytest
✅ Git initialization
✅ Requirements files (prod + dev)
✅ README with documentation
✅ .gitignore file
✅ API examples

## Advanced Features

### Smart Scaffolding

After creating your project, add components easily:

```bash
cd my-api

# Add a model
projex add model Product --fields name:str,price:float,stock:int

# Add CRUD endpoints
projex add endpoint products --crud

# Add a service
projex add service payment --async
```

### CI/CD Setup

```bash
# Add GitHub Actions
projex add cicd --provider github

# Or GitLab CI
projex add cicd --provider gitlab
```

### Environment Management

```bash
# Create environment files
projex env add development
projex env add staging
projex env add production

# List environments
projex env list
```

### Dependency Management

```bash
# Check for outdated packages
projex deps check

# Update packages safely
projex deps update

# Security audit
projex deps audit
```

### Documentation

```bash
# Add MkDocs documentation
projex add docs --tool mkdocs

# Start docs server
mkdocs serve
```

### Testing

```bash
# Enhanced test configuration
projex add test-config --enhanced

# Run tests
pytest

# With coverage
pytest --cov=app
```

### Project Validation

```bash
# Validate project structure
projex validate

# Show project info
projex info
```

## Need Help?

* 📖 Read the full [README.md](README.md)
* 📚 Check [EXAMPLES.md](EXAMPLES.md) for more examples
* 🐛 [Report bugs](https://github.com/ChAbdulWahhab/projex/issues)
* 💬 [Ask questions](https://github.com/ChAbdulWahhab/projex/discussions)
* 🤝 [Contribute](CONTRIBUTING.md)

Happy coding! 🎉