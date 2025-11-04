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
    },
    'bottle': {
        'description': 'Fast and simple micro-framework for small web applications',
        'features': [
            'Single file framework',
            'Built-in development server',
            'Template engine',
            'Simple routing',
            'CORS support',
            'WSGI compatible',
            'Docker support',
            'pytest setup'
        ],
        'dependencies': [
            'bottle>=0.12.25',
            'python-dotenv>=1.0.0',
            'gunicorn>=21.2.0',
            'psycopg2-binary>=2.9.9',
        ],
        'dev_dependencies': [
            'pytest>=7.4.0',
            'pytest-bottle>=0.1.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
        ]
    },
    'pyramid': {
        'description': 'Flexible web framework for large applications',
        'features': [
            'Flexible architecture',
            'Traversal and URL dispatch',
            'Security policies',
            'SQLAlchemy integration',
            'Alembic migrations',
            'CORS support',
            'Docker support',
            'pytest setup'
        ],
        'dependencies': [
            'pyramid>=2.0.2',
            'waitress>=2.1.2',
            'sqlalchemy>=2.0.0',
            'alembic>=1.12.0',
            'zope.sqlalchemy>=2.0',
            'python-dotenv>=1.0.0',
            'psycopg2-binary>=2.9.9',
            'pyramid-cors>=0.1',
        ],
        'dev_dependencies': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'webtest>=3.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
        ]
    },
    'tornado': {
        'description': 'Asynchronous web framework and networking library',
        'features': [
            'Async/await support',
            'Non-blocking I/O',
            'WebSocket support',
            'SQLAlchemy integration',
            'JWT authentication',
            'CORS support',
            'Docker support',
            'pytest setup'
        ],
        'dependencies': [
            'tornado>=6.4.0',
            'sqlalchemy>=2.0.0',
            'alembic>=1.12.0',
            'python-dotenv>=1.0.0',
            'psycopg2-binary>=2.9.9',
            'python-jose[cryptography]>=3.3.0',
            'passlib[bcrypt]>=1.7.4',
        ],
        'dev_dependencies': [
            'pytest>=7.4.0',
            'pytest-tornado>=0.8.1',
            'pytest-asyncio>=0.21.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
        ]
    },
    'sanic': {
        'description': 'Fast async web framework built on uvloop',
        'features': [
            'Async/await support',
            'High performance',
            'Built-in async ORM',
            'Automatic API docs',
            'WebSocket support',
            'CORS support',
            'Docker support',
            'pytest setup'
        ],
        'dependencies': [
            'sanic>=23.12.0',
            'sanic-ext>=23.12.0',
            'sanic-cors>=2.0.0',
            'python-dotenv>=1.0.0',
            'psycopg2-binary>=2.9.9',
            'asyncpg>=0.29.0',
        ],
        'dev_dependencies': [
            'pytest>=7.4.0',
            'pytest-asyncio>=0.21.0',
            'pytest-sanic>=1.1.0',
            'httpx>=0.25.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
        ]
    },
    'cherrypy': {
        'description': 'Minimalist Python web framework',
        'features': [
            'Object-oriented design',
            'Built-in HTTP server',
            'Plugin system',
            'Session management',
            'CORS support',
            'RESTful routing',
            'Docker support',
            'pytest setup'
        ],
        'dependencies': [
            'cherrypy>=18.9.0',
            'python-dotenv>=1.0.0',
            'sqlalchemy>=2.0.0',
            'psycopg2-binary>=2.9.9',
            'cherrypy-cors>=1.0.0',
        ],
        'dev_dependencies': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
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

4. Setup database:
```bash
# For PostgreSQL/MySQL: Run migrations
# For FastAPI: alembic upgrade head
# For Django: python manage.py migrate
# For Flask: flask db upgrade
```

5. Run the application:
```bash
{run_command}
```

## Project Structure

```
{project_structure}
```

## Database Setup

The project is configured to use {database_type}. Update the `DATABASE_URL` in `.env` file with your database credentials.

### Using Docker

```bash
docker-compose up -d
```

This will start the application and database service.

### Manual Database Setup

1. Install and start your database server
2. Update `DATABASE_URL` in `.env` file
3. Run migrations (see step 4 in Setup)

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