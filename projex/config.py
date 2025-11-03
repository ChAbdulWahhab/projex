"""Configuration for available templates and their settings"""

AVAILABLE_TEMPLATES = {
    'fastapi': {
        'description': 'Modern, fast API framework with async support',
        'features': [
            'Async/await support',
            'Automatic API documentation',
            'Pydantic models',
            'SQLAlchemy integration',
            'Alembic migrations',
            'JWT authentication',
            'Docker support',
            'pytest setup'
        ],
        'dependencies': [
            'fastapi>=0.104.0',
            'uvicorn[standard]>=0.24.0',
            'sqlalchemy>=2.0.0',
            'alembic>=1.12.0',
            'pydantic>=2.5.0',
            'pydantic-settings>=2.1.0',
            'python-jose[cryptography]>=3.3.0',
            'passlib[bcrypt]>=1.7.4',
            'python-multipart>=0.0.6',
            'psycopg2-binary>=2.9.9',
        ],
        'dev_dependencies': [
            'pytest>=7.4.0',
            'pytest-asyncio>=0.21.0',
            'httpx>=0.25.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.7.0',
        ]
    },
    'django': {
        'description': 'Batteries-included web framework for perfectionists',
        'features': [
            'Django REST Framework',
            'Admin panel',
            'ORM with migrations',
            'Authentication system',
            'Custom user model',
            'CORS headers',
            'Environment variables',
            'pytest-django setup'
        ],
        'dependencies': [
            'Django>=4.2.0',
            'djangorestframework>=3.14.0',
            'django-cors-headers>=4.3.0',
            'django-environ>=0.11.0',
            'psycopg2-binary>=2.9.9',
            'pillow>=10.1.0',
            'django-filter>=23.5',
            'drf-spectacular>=0.27.0',
        ],
        'dev_dependencies': [
            'pytest>=7.4.0',
            'pytest-django>=4.7.0',
            'factory-boy>=3.3.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'django-debug-toolbar>=4.2.0',
        ]
    },
    'flask': {
        'description': 'Lightweight and flexible web framework',
        'features': [
            'Flask-RESTful',
            'Flask-SQLAlchemy',
            'Flask-Migrate',
            'Flask-JWT-Extended',
            'Flask-CORS',
            'Blueprints structure',
            'Config management',
            'pytest setup'
        ],
        'dependencies': [
            'Flask>=3.0.0',
            'Flask-RESTful>=0.3.10',
            'Flask-SQLAlchemy>=3.1.0',
            'Flask-Migrate>=4.0.5',
            'Flask-JWT-Extended>=4.5.3',
            'Flask-CORS>=4.0.0',
            'python-dotenv>=1.0.0',
            'psycopg2-binary>=2.9.9',
            'marshmallow>=3.20.0',
        ],
        'dev_dependencies': [
            'pytest>=7.4.0',
            'pytest-flask>=1.3.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'Flask-Testing>=0.8.1',
        ]
    }
}

# Common files for all templates
COMMON_FILES = {
    '.gitignore': '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Environment variables
.env
.env.local

# Database
*.db
*.sqlite3
db.sqlite3

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
''',
    
    '.env.example': '''# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Security
SECRET_KEY=your-secret-key-here

# Environment
DEBUG=True
ENVIRONMENT=development
''',
    
    'README.md': '''# {project_name}

{description}

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
{run_command}
```

## Project Structure

```
{project_structure}
```

## API Documentation

{api_docs_info}

## Testing

```bash
pytest
```

## Author

{author}
''',

    'Dockerfile': '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

{docker_cmd}
''',

    'docker-compose.yml': '''version: '3.8'

services:
  web:
    build: .
    ports:
      - "{port}:{port}"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/appdb
      - DEBUG=True
    depends_on:
      - db
    volumes:
      - .:/app

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
''',

    'pytest.ini': '''[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
'''
}