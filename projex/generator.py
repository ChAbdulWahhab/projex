import os
import subprocess
from pathlib import Path
from jinja2 import Template
from typing import Optional
import shutil

from .config import AVAILABLE_TEMPLATES, COMMON_FILES


class ProjectGenerator:
    def __init__(
        self,
        project_name: str,
        template_type: str,
        base_path: str = '.',
        author: str = 'Developer',
        description: str = '',
        init_git: bool = True,
        create_venv: bool = True
    ):
        self.project_name = project_name
        self.template_type = template_type
        self.base_path = Path(base_path)
        self.author = author
        self.description = description or f"A {template_type} project"
        self.init_git = init_git
        self.create_venv = create_venv
        
        self.project_path = self.base_path / project_name
        self.template_config = AVAILABLE_TEMPLATES[template_type]
    
    def generate(self) -> Path:
        """Generate the complete project"""
        if self.project_path.exists():
            raise FileExistsError(f"Project directory {self.project_path} already exists")
        
        # Create project directory
        self.project_path.mkdir(parents=True)
        
        # Generate based on template type
        if self.template_type == 'fastapi':
            self._generate_fastapi()
        elif self.template_type == 'django':
            self._generate_django()
        elif self.template_type == 'flask':
            self._generate_flask()
        
        # Create common files
        self._create_common_files()
        
        # Create requirements files
        self._create_requirements()
        
        # Initialize git
        if self.init_git:
            self._init_git()
        
        # Create virtual environment
        if self.create_venv:
            self._create_virtualenv()
        
        return self.project_path
    
    def _generate_fastapi(self):
        """Generate FastAPI project structure"""
        app_dir = self.project_path / 'app'
        app_dir.mkdir()
        
        # Create __init__.py
        (app_dir / '__init__.py').write_text('')
        
        # Create main.py
        main_content = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Welcome to ''' + self.project_name + '''"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
'''
        (app_dir / 'main.py').write_text(main_content)
        
        # Create core directory
        core_dir = app_dir / 'core'
        core_dir.mkdir()
        (core_dir / '__init__.py').write_text('')
        
        config_content = '''from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "''' + self.project_name + '''"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    DATABASE_URL: str = "sqlite:///./app.db"
    
    class Config:
        env_file = ".env"


settings = Settings()
'''
        (core_dir / 'config.py').write_text(config_content)
        
        # Create database module
        (core_dir / 'database.py').write_text('''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
''')
        
        # Create API structure
        api_dir = app_dir / 'api' / 'v1'
        api_dir.mkdir(parents=True)
        (app_dir / 'api' / '__init__.py').write_text('')
        (api_dir / '__init__.py').write_text('')
        
        (api_dir / 'router.py').write_text('''from fastapi import APIRouter
from app.api.v1.endpoints import items

api_router = APIRouter()
api_router.include_router(items.router, prefix="/items", tags=["items"])
''')
        
        # Create endpoints
        endpoints_dir = api_dir / 'endpoints'
        endpoints_dir.mkdir()
        (endpoints_dir / '__init__.py').write_text('')
        
        (endpoints_dir / 'items.py').write_text('''from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    id: int
    name: str
    description: str = None


# Mock database
items_db = [
    Item(id=1, name="Item 1", description="First item"),
    Item(id=2, name="Item 2", description="Second item"),
]


@router.get("/", response_model=List[Item])
async def get_items():
    return items_db


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/", response_model=Item)
async def create_item(item: Item):
    items_db.append(item)
    return item
''')
        
        # Create models and schemas directories
        (app_dir / 'models').mkdir()
        (app_dir / 'models' / '__init__.py').write_text('')
        (app_dir / 'schemas').mkdir()
        (app_dir / 'schemas' / '__init__.py').write_text('')
        
        # Create tests
        tests_dir = self.project_path / 'tests'
        tests_dir.mkdir()
        (tests_dir / '__init__.py').write_text('')
        (tests_dir / 'test_main.py').write_text('''from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
''')
    
    def _generate_django(self):
        """Generate Django project structure"""
        # Django needs to be installed to run django-admin
        # We'll create the basic structure manually
        
        project_slug = self.project_name.replace('-', '_').replace(' ', '_').lower()
        
        # Create config directory (Django project settings)
        config_dir = self.project_path / 'config'
        config_dir.mkdir()
        (config_dir / '__init__.py').write_text('')
        
        # Settings
        settings_content = f'''import os
from pathlib import Path
import environ

env = environ.Env(DEBUG=(bool, False))

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-this')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'apps.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {{
    'default': env.db('DATABASE_URL', default='sqlite:///db.sqlite3')
}}

AUTH_PASSWORD_VALIDATORS = [
    {{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS
CORS_ALLOW_ALL_ORIGINS = DEBUG

# REST Framework
REST_FRAMEWORK = {{
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}}
'''
        (config_dir / 'settings.py').write_text(settings_content)
        
        # URLs
        (config_dir / 'urls.py').write_text('''from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.core.urls')),
]
''')
        
        # WSGI
        (config_dir / 'wsgi.py').write_text(f'''import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
''')
        
        # ASGI
        (config_dir / 'asgi.py').write_text(f'''import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_asgi_application()
''')
        
        # manage.py
        (self.project_path / 'manage.py').write_text('''#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)
''')
        
        # Make manage.py executable
        os.chmod(self.project_path / 'manage.py', 0o755)
        
        # Create apps directory
        apps_dir = self.project_path / 'apps'
        apps_dir.mkdir()
        (apps_dir / '__init__.py').write_text('')
        
        # Create core app
        core_dir = apps_dir / 'core'
        core_dir.mkdir()
        (core_dir / '__init__.py').write_text('')
        (core_dir / 'admin.py').write_text('from django.contrib import admin\n')
        (core_dir / 'apps.py').write_text('''from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
''')
        (core_dir / 'models.py').write_text('from django.db import models\n')
        (core_dir / 'views.py').write_text('''from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'healthy'})
''')
        (core_dir / 'urls.py').write_text('''from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health'),
]
''')
        
        # Create tests
        (core_dir / 'tests.py').write_text('''from django.test import TestCase
from django.urls import reverse


class HealthCheckTest(TestCase):
    def test_health_check(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'healthy'})
''')
    
    def _generate_flask(self):
        """Generate Flask project structure"""
        app_dir = self.project_path / 'app'
        app_dir.mkdir()
        
        # Create __init__.py with app factory
        init_content = '''from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return {'message': 'Welcome to ''' + self.project_name + ''''}
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}
    
    return app
'''
        (app_dir / '__init__.py').write_text(init_content)
        
        # Create config.py
        config_content = '''import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \\
        'sqlite:///' + os.path.join(basedir, '..', 'app.db')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
'''
        (app_dir / 'config.py').write_text(config_content)
        
        # Create api blueprint
        api_dir = app_dir / 'api'
        api_dir.mkdir()
        (api_dir / '__init__.py').write_text('''from flask import Blueprint

api_bp = Blueprint('api', __name__)

from app.api import routes
''')
        
        (api_dir / 'routes.py').write_text('''from flask import jsonify, request
from app.api import api_bp


@api_bp.route('/items', methods=['GET'])
def get_items():
    items = [
        {'id': 1, 'name': 'Item 1', 'description': 'First item'},
        {'id': 2, 'name': 'Item 2', 'description': 'Second item'},
    ]
    return jsonify(items)


@api_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    # Mock data
    item = {'id': item_id, 'name': f'Item {item_id}'}
    return jsonify(item)


@api_bp.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    # Process and save item
    return jsonify(data), 201
''')
        
        # Create models directory
        models_dir = app_dir / 'models'
        models_dir.mkdir()
        (models_dir / '__init__.py').write_text('from app import db\n')
        
        # Create run.py
        (self.project_path / 'run.py').write_text('''from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
''')
        
        # Create tests
        tests_dir = self.project_path / 'tests'
        tests_dir.mkdir()
        (tests_dir / '__init__.py').write_text('')
        (tests_dir / 'test_api.py').write_text('''import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app('development')
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'message' in response.data


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'healthy'}
''')
    
    def _create_common_files(self):
        """Create common files like .gitignore, README, etc."""
        context = {
            'project_name': self.project_name,
            'description': self.description,
            'author': self.author,
            'run_command': self._get_run_command(),
            'project_structure': self._get_project_structure(),
            'api_docs_info': self._get_api_docs_info(),
            'docker_cmd': self._get_docker_cmd(),
            'port': self._get_default_port()
        }
        
        for filename, content in COMMON_FILES.items():
            template = Template(content)
            rendered = template.render(**context)
            (self.project_path / filename).write_text(rendered)
    
    def _create_requirements(self):
        """Create requirements.txt and requirements-dev.txt"""
        deps = self.template_config['dependencies']
        dev_deps = self.template_config['dev_dependencies']
        
        (self.project_path / 'requirements.txt').write_text('\n'.join(deps))
        (self.project_path / 'requirements-dev.txt').write_text(
            '-r requirements.txt\n' + '\n'.join(dev_deps)
        )
    
    def _init_git(self):
        """Initialize git repository"""
        try:
            subprocess.run(['git', 'init'], cwd=self.project_path, check=True, 
                         capture_output=True)
            subprocess.run(['git', 'add', '.'], cwd=self.project_path, check=True,
                         capture_output=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit'], 
                         cwd=self.project_path, check=True, capture_output=True)
        except subprocess.CalledProcessError:
            pass  # Git might not be installed
    
    def _create_virtualenv(self):
        """Create virtual environment"""
        try:
            subprocess.run(['python', '-m', 'venv', 'venv'], 
                         cwd=self.project_path, check=True, capture_output=True)
        except subprocess.CalledProcessError:
            pass  # Venv creation failed
    
    def _get_run_command(self):
        commands = {
            'fastapi': 'uvicorn app.main:app --reload',
            'django': 'python manage.py runserver',
            'flask': 'python run.py'
        }
        return commands.get(self.template_type, '')
    
    def _get_project_structure(self):
        structures = {
            'fastapi': 'app/\n├── main.py\n├── core/\n├── api/\n├── models/\n└── schemas/',
            'django': 'config/\napps/\n├── core/\nmanage.py',
            'flask': 'app/\n├── __init__.py\n├── api/\n├── models/\nrun.py'
        }
        return structures.get(self.template_type, '')
    
    def _get_api_docs_info(self):
        docs = {
            'fastapi': 'Visit http://localhost:8000/docs for Swagger UI',
            'django': 'API endpoints available at /api/',
            'flask': 'API endpoints available at /api/'
        }
        return docs.get(self.template_type, '')
    
    def _get_docker_cmd(self):
        cmds = {
            'fastapi': 'CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]',
            'django': 'CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]',
            'flask': 'CMD ["python", "run.py"]'
        }
        return cmds.get(self.template_type, '')
    
    def _get_default_port(self):
        ports = {
            'fastapi': '8000',
            'django': '8000',
            'flask': '5000'
        }
        return ports.get(self.template_type, '8000')