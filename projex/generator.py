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
        create_venv: bool = True,
        database: Optional[str] = None,
        style: str = 'standard',
        auth: Optional[str] = None
    ):
        self.project_name = project_name
        self.template_type = template_type
        self.base_path = Path(base_path)
        self.author = author
        self.description = description or f"A {template_type} project"
        self.init_git = init_git
        self.create_venv = create_venv
        self.database = database or 'postgresql'  # Default to PostgreSQL
        self.style = style.lower()  # minimal, standard, full
        self.auth = auth  # jwt, oauth2, apikey, basic
        
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
        elif self.template_type == 'bottle':
            self._generate_bottle()
        elif self.template_type == 'pyramid':
            self._generate_pyramid()
        elif self.template_type == 'tornado':
            self._generate_tornado()
        elif self.template_type == 'sanic':
            self._generate_sanic()
        elif self.template_type == 'cherrypy':
            self._generate_cherrypy()
        
        # Setup database configuration (skip for minimal style)
        if self.style != 'minimal':
            self._setup_database()
        
        # Setup authentication (skip for minimal style)
        if self.style != 'minimal' and self.auth:
            self._setup_authentication()
        
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
        
        # Post-generation validation
        self._validate_generation()
        
        return self.project_path
    
    def _read_welcome_template(self, framework: str) -> str:
        """Read the bundled welcome.html for a framework from projex/templates.

        Falls back to a minimal HTML if file not found.
        """
        try:
            here = Path(__file__).resolve().parent
            tpl = here / 'templates' / framework / 'welcome.html'
            if tpl.exists():
                return tpl.read_text(encoding='utf-8')
        except Exception:
            pass
        return '<!doctype html><title>Welcome</title><h1>Welcome</h1>'
    
    def _generate_fastapi(self):
        """Generate FastAPI project structure"""
        app_dir = self.project_path / 'app'
        app_dir.mkdir()
        
        # Create __init__.py
        (app_dir / '__init__.py').write_text('')
        
        # Create main.py
        welcome_html = self._read_welcome_template('fastapi')
        main_content = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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

WELCOME_TEMPLATE = r"""''' + welcome_html.replace('"""', '\\"""') + '''"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(WELCOME_TEMPLATE)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
    

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello, {name}!"}
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
        
        # Create tests (skip for minimal style)
        if self.style != 'minimal':
            tests_dir = self.project_path / 'tests'
            tests_dir.mkdir()
            (tests_dir / '__init__.py').write_text('')
            (tests_dir / 'test_main.py').write_text('''from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Your server is running" in response.text


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_hello_endpoint():
    response = client.get("/hello/Alice")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Alice!"}
''')
    
    def _generate_django(self):
        """Generate Django project structure"""
        # Django needs to be installed to run django-admin
        # We'll create the basic structure manually
        
        # Read welcome template
        welcome_html = self._read_welcome_template('django')
        
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
from apps.core.views import index

urlpatterns = [
    path('', index, name='index'),
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
from django.http import HttpResponse

WELCOME_TEMPLATE = r"""''' + welcome_html.replace('"""', '\\"""') + '''"""


def index(request):
    return HttpResponse(WELCOME_TEMPLATE)


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'healthy'})


@api_view(['GET'])
def hello(request, name: str):
    return Response({'message': f'Hello, {name}!'})
''')
        (core_dir / 'urls.py').write_text('''from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health'),
    path('hello/<str:name>/', views.hello, name='hello'),
]
''')
        
        # Create tests (skip for minimal style)
        if self.style != 'minimal':
            (core_dir / 'tests.py').write_text('''from django.test import TestCase
from django.urls import reverse


class HealthCheckTest(TestCase):
    def test_health_check(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'healthy'})

    def test_hello(self):
        response = self.client.get(reverse('hello', kwargs={'name': 'World'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Hello, World!'})
''')
    
    def _generate_flask(self):
        """Generate Flask project structure"""
        app_dir = self.project_path / 'app'
        app_dir.mkdir()
        
        # Read welcome template
        welcome_html = self._read_welcome_template('flask')
        
        # Create __init__.py with app factory
        init_content = '''from flask import Flask, render_template_string, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

WELCOME_TEMPLATE = r"""''' + welcome_html.replace('"""', '\\"""') + '''"""


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
        return render_template_string(WELCOME_TEMPLATE)
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}
    
    @app.route('/hello/<name>')
    def hello(name):
        return jsonify({'message': f'Hello, {name}!'}), 200
    
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
        
        # Create tests (skip for minimal style)
        if self.style != 'minimal':
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
    assert b'Your server is running' in response.data


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'healthy'}


def test_hello(client):
    response = client.get('/hello/Alice')
    assert response.status_code == 200
    assert response.json == {'message': 'Hello, Alice!'}
''')
    
    def _generate_bottle(self):
        """Generate Bottle project structure"""
        app_dir = self.project_path / 'app'
        app_dir.mkdir()
        
        # Create __init__.py
        (app_dir / '__init__.py').write_text('')
        
        # Read welcome template
        welcome_html = self._read_welcome_template('bottle')
        
        # Create main.py
        main_content = f'''import os
from bottle import Bottle, run, request, response
from bottle import HTTPResponse
from dotenv import load_dotenv

load_dotenv()

app = Bottle()

WELCOME_TEMPLATE = r"""''' + welcome_html.replace('"""', '\\"""') + f'''"""


def enable_cors():
    """Enable CORS for all routes"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'


@app.hook('after_request')
def after_request():
    enable_cors()


@app.route('/')
def index():
    return HTTPResponse(WELCOME_TEMPLATE)


@app.route('/health')
def health():
    return {{"status": "healthy"}}


@app.route('/hello/<name>')
def hello(name):
    return {{"message": f"Hello, {name}!"}}


@app.route('/api/items', method='GET')
def get_items():
    items = [
        {{"id": 1, "name": "Item 1", "description": "First item"}},
        {{"id": 2, "name": "Item 2", "description": "Second item"}},
    ]
    return {{"items": items}}


@app.route('/api/items/<item_id:int>', method='GET')
def get_item(item_id):
    item = {{"id": item_id, "name": f"Item {{item_id}}"}}
    return item


@app.route('/api/items', method='POST')
def create_item():
    data = request.json
    return {{"message": "Item created", "data": data}}, 201


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    run(app, host='0.0.0.0', port=port, debug=debug, reloader=debug)
'''
        (app_dir / 'main.py').write_text(main_content)
        
        # Create config.py
        config_content = '''import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    PORT = int(os.getenv('PORT', 8000))
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')


config = Config()
'''
        (app_dir / 'config.py').write_text(config_content)
        
        # Create routes directory
        routes_dir = app_dir / 'routes'
        routes_dir.mkdir()
        (routes_dir / '__init__.py').write_text('')
        
        # Create models directory
        models_dir = app_dir / 'models'
        models_dir.mkdir()
        (models_dir / '__init__.py').write_text('')
        
        # Create tests (skip for minimal style)
        if self.style != 'minimal':
            tests_dir = self.project_path / 'tests'
            tests_dir.mkdir()
            (tests_dir / '__init__.py').write_text('')
            (tests_dir / 'test_main.py').write_text('''import pytest
from bottle import Bottle
from app.main import app


def test_root():
    response = app.get('/')
    assert response.status_code == 200
    data = response.json
    assert 'message' in data


def test_health():
    response = app.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}
''')
    
    def _generate_pyramid(self):
        """Generate Pyramid project structure"""
        app_dir = self.project_path / 'app'
        app_dir.mkdir()
        
        # Create __init__.py
        (app_dir / '__init__.py').write_text('')
        
        # Read welcome template
        welcome_html = self._read_welcome_template('pyramid')
        
        # Create main.py
        main_content = f'''from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from dotenv import load_dotenv
import os

load_dotenv()

WELCOME_TEMPLATE = r"""''' + welcome_html.replace('"""', '\\"""') + f'''"""


@view_config(route_name='home')
def home(request):
    return Response(WELCOME_TEMPLATE)


@view_config(route_name='health', renderer='json')
def health(request):
    return {{"status": "healthy"}}


@view_config(route_name='items', renderer='json', request_method='GET')
def get_items(request):
    items = [
        {{"id": 1, "name": "Item 1", "description": "First item"}},
        {{"id": 2, "name": "Item 2", "description": "Second item"}},
    ]
    return {{"items": items}}


@view_config(route_name='hello', renderer='json')
def hello(request):
    name = request.matchdict.get('name', 'World')
    return {{"message": f"Hello, {name}!"}}


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    config = Configurator(settings=settings)
    
    # CORS
    config.add_cors_preflight_handler()
    config.add_route('home', '/')
    config.add_route('health', '/health')
    config.add_route('items', '/api/items')
    config.add_route('hello', '/hello/{name}')
    config.scan()
    
    return config.make_wsgi_app()
'''
        (app_dir / 'main.py').write_text(main_content)
        
        # Create config.py
        config_content = '''import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')
    database_url = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    environment = os.getenv('ENVIRONMENT', 'development')
'''
        (app_dir / 'config.py').write_text(config_content)
        
        # Create routes directory
        routes_dir = app_dir / 'routes'
        routes_dir.mkdir()
        (routes_dir / '__init__.py').write_text('')
        
        # Create models directory
        models_dir = app_dir / 'models'
        models_dir.mkdir()
        (models_dir / '__init__.py').write_text('')
        
        # Create development.ini
        dev_ini = '''[app:main]
use = egg:waitress#main
listen = 0.0.0.0:8000

[server:main]
use = egg:waitress#main
listen = 0.0.0.0:8000
'''
        (self.project_path / 'development.ini').write_text(dev_ini)
        
        # Create run.py
        (self.project_path / 'run.py').write_text('''from pyramid.paster import get_app
import os

if __name__ == '__main__':
    app = get_app('development.ini', 'main')
    from waitress import serve
    serve(app, host='0.0.0.0', port=8000)
''')
        
        # Create tests (skip for minimal style)
        if self.style != 'minimal':
            tests_dir = self.project_path / 'tests'
            tests_dir.mkdir()
            (tests_dir / '__init__.py').write_text('')
            (tests_dir / 'test_main.py').write_text('''from pyramid.testing import DummyRequest
from app.main import home, health, get_items


def test_home():
    request = DummyRequest()
    response = home(request)
    assert 'message' in response


def test_health():
    request = DummyRequest()
    response = health(request)
    assert response == {"status": "healthy"}


def test_get_items():
    request = DummyRequest()
    response = get_items(request)
    assert 'items' in response
    assert len(response['items']) == 2
''')
    
    def _generate_tornado(self):
        """Generate Tornado project structure"""
        app_dir = self.project_path / 'app'
        app_dir.mkdir()
        
        # Create __init__.py
        (app_dir / '__init__.py').write_text('')
        
        # Read welcome template
        welcome_html = self._read_welcome_template('tornado')
        
        # Create main.py
        main_content = f'''import tornado.ioloop
import tornado.web
import tornado.options
import os
from dotenv import load_dotenv

load_dotenv()

tornado.options.define("port", default=8000, help="run on the given port", type=int)

WELCOME_TEMPLATE = r"""''' + welcome_html.replace('"""', '\\"""') + f'''"""


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(WELCOME_TEMPLATE)


class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({{"status": "healthy"}})


class ItemsHandler(tornado.web.RequestHandler):
    def get(self):
        items = [
            {{"id": 1, "name": "Item 1", "description": "First item"}},
            {{"id": 2, "name": "Item 2", "description": "Second item"}},
        ]
        self.write({{"items": items}})
    
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        self.write({{"message": "Item created", "data": data}})
        self.set_status(201)


class ItemHandler(tornado.web.RequestHandler):
    def get(self, item_id):
        item = {{"id": int(item_id), "name": f"Item {{item_id}}"}}
        self.write(item)


class HelloHandler(tornado.web.RequestHandler):
    def get(self, name):
        self.write({{"message": f"Hello, {{name}}!"}})


def make_app():
    settings = {{
        "debug": os.getenv("DEBUG", "True").lower() == "true",
    }}
    
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/health", HealthHandler),
        (r"/api/items", ItemsHandler),
        (r"/api/items/([0-9]+)", ItemHandler),
        (r"/hello/([A-Za-z0-9_%-]+)", HelloHandler),
    ], **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
'''
        (app_dir / 'main.py').write_text(main_content)
    
    def _generate_sanic(self):
        """Generate Sanic project structure"""
        app_dir = self.project_path / 'app'
        app_dir.mkdir()
        
        # Create __init__.py
        (app_dir / '__init__.py').write_text('')
        
        # Read welcome template
        welcome_html = self._read_welcome_template('sanic')
        
        # Create main.py
        main_content = f'''from sanic import Sanic
from sanic.response import json, html
from sanic_ext import Extend
from sanic_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Sanic("{self.project_name}")

# Enable CORS
CORS(app, resources={{r"/api/*": {{"origins": "*"}}}})

# Enable OpenAPI docs
Extend(app)

WELCOME_TEMPLATE = r"""''' + welcome_html.replace('"""', '\\"""') + f'''"""


@app.get("/")
async def index(request):
    return html(WELCOME_TEMPLATE)

@app.get("/hello/<name>")
async def hello(request, name: str):
    return json({"message": f"Hello, {name}!"})

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))
    app.run(host="0.0.0.0", port=port, debug=True, auto_reload=True)
'''
        (app_dir / 'main.py').write_text(main_content)
        
        # Create config.py
        config_content = '''import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    PORT = int(os.getenv('PORT', 8000))
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
'''
        (app_dir / 'config.py').write_text(config_content)
        
        # Create routes directory
        routes_dir = app_dir / 'routes'
        routes_dir.mkdir()
        (routes_dir / '__init__.py').write_text('')
        
        # Create models directory
        models_dir = app_dir / 'models'
        models_dir.mkdir()
        (models_dir / '__init__.py').write_text('')
        
        # Create tests (skip for minimal style)
        if self.style != 'minimal':
            tests_dir = self.project_path / 'tests'
            tests_dir.mkdir()
            (tests_dir / '__init__.py').write_text('')
            (tests_dir / 'test_main.py').write_text('''import pytest
from tornado.testing import AsyncHTTPTestCase
from app.main import make_app


class TestApp(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()
    
    def test_root(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        import json
        data = json.loads(response.body)
        self.assertIn('message', data)
    
    def test_health(self):
        response = self.fetch('/health')
        self.assertEqual(response.code, 200)
        import json
        data = json.loads(response.body)
        self.assertEqual(data, {"status": "healthy"})
''')
    
    def _generate_cherrypy(self):
        """Generate CherryPy project structure"""
        app_dir = self.project_path / 'app'
        app_dir.mkdir()
        
        # Create __init__.py
        (app_dir / '__init__.py').write_text('')
        
        # Read welcome template
        welcome_html = self._read_welcome_template('cherrypy')
        
        # Create main.py
        main_content = f'''import cherrypy
import os
from dotenv import load_dotenv

load_dotenv()

WELCOME_TEMPLATE = r"""''' + welcome_html.replace('"""', '\\"""') + f'''"""


class Root:
    @cherrypy.expose
    def index(self):
        return WELCOME_TEMPLATE
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def health(self):
        return {"status": "healthy"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def hello(self, name):
        return {"message": f"Hello, {name}!"}


class ItemsAPI:
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        items = [
            {{"id": 1, "name": "Item 1", "description": "First item"}},
            {{"id": 2, "name": "Item 2", "description": "Second item"}},
        ]
        return {{"items": items}}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def default(self, item_id=None):
        if cherrypy.request.method == 'GET' and item_id:
            return {{"id": int(item_id), "name": "Item " + str(item_id)}}
        elif cherrypy.request.method == 'POST':
            data = cherrypy.request.json
            cherrypy.response.status = 201
            return {{"message": "Item created", "data": data}}


def setup_cors():
    """Enable CORS"""
    def cors_tool():
        if cherrypy.request.method == 'OPTIONS':
            cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
            cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            cherrypy.response.status = 200
            return True
        else:
            cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
    
    cherrypy.tools.cors = cherrypy.Tool('before_handler', cors_tool)


def make_app():
    setup_cors()
    
    config = {{
        '/': {{
            'tools.cors.on': True,
            'tools.json_out.on': True,
        }},
        '/api': {{
            'tools.cors.on': True,
            'tools.json_in.on': True,
            'tools.json_out.on': True,
        }},
        '/api/items': {{
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        }}
    }}
    
    root = Root()
    root.api = ItemsAPI()
    
    return root, config


if __name__ == '__main__':
    root, config = make_app()
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    cherrypy.config.update({{
        'server.socket_host': '0.0.0.0',
        'server.socket_port': port,
        'tools.sessions.on': True,
        'tools.encode.on': True,
        'tools.encode.encoding': 'utf-8',
        'log.screen': debug,
    }})
    
    cherrypy.quickstart(root, '/', config)
'''
        (app_dir / 'main.py').write_text(main_content)
        
        # Create config.py
        config_content = '''import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    PORT = int(os.getenv('PORT', 8000))
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
'''
        (app_dir / 'config.py').write_text(config_content)
        
        # Create routes directory
        routes_dir = app_dir / 'routes'
        routes_dir.mkdir()
        (routes_dir / '__init__.py').write_text('')
        
        # Create models directory
        models_dir = app_dir / 'models'
        models_dir.mkdir()
        (models_dir / '__init__.py').write_text('')
        
        # Create tests (skip for minimal style)
        if self.style != 'minimal':
            tests_dir = self.project_path / 'tests'
            tests_dir.mkdir()
            (tests_dir / '__init__.py').write_text('')
            (tests_dir / 'test_main.py').write_text('''import pytest
import cherrypy
from app.main import Root, ItemsAPI


class TestRoot:
    def test_index(self):
        root = Root()
        result = root.index()
        assert 'message' in result
    
    def test_health(self):
        root = Root()
        result = root.health()
        assert result == {"status": "healthy"}


class TestItemsAPI:
    def test_index(self):
        api = ItemsAPI()
        result = api.index()
        assert 'items' in result
        assert len(result['items']) == 2
''')
    
    def _setup_database(self):
        """Setup database configuration based on selected database type"""
        db_type = self.database.lower()
        
        # Database configuration
        db_configs = {
            'postgresql': {
                'url': 'postgresql://user:password@localhost:5432/dbname',
                'docker_url': 'postgresql://postgres:postgres@db:5432/appdb',
                'packages': ['psycopg2-binary>=2.9.9'],
                'docker_image': 'postgres:15',
                'docker_env': {
                    'POSTGRES_DB': 'appdb',
                    'POSTGRES_USER': 'postgres',
                    'POSTGRES_PASSWORD': 'postgres'
                }
            },
            'mysql': {
                'url': 'mysql+pymysql://user:password@localhost:3306/dbname',
                'docker_url': 'mysql+pymysql://root:root@db:3306/appdb',
                'packages': ['pymysql>=1.1.0', 'cryptography>=41.0.0'],
                'docker_image': 'mysql:8.0',
                'docker_env': {
                    'MYSQL_DATABASE': 'appdb',
                    'MYSQL_USER': 'root',
                    'MYSQL_ROOT_PASSWORD': 'root'
                }
            },
            'mongodb': {
                'url': 'mongodb://localhost:27017/dbname',
                'docker_url': 'mongodb://db:27017/appdb',
                'packages': ['motor>=3.3.0', 'pymongo>=4.6.0'],
                'docker_image': 'mongo:7',
                'docker_env': {}
            },
            'sqlite': {
                'url': 'sqlite:///./app.db',
                'docker_url': 'sqlite:///./app.db',
                'packages': [],
                'docker_image': None,
                'docker_env': {}
            },
            'redis': {
                'url': 'redis://localhost:6379/0',
                'docker_url': 'redis://db:6379/0',
                'packages': ['redis>=5.0.0', 'hiredis>=2.2.0'],
                'docker_image': 'redis:7-alpine',
                'docker_env': {}
            }
        }
        
        config = db_configs.get(db_type, db_configs['postgresql'])
        
        # Update database configuration in existing config files
        self._update_database_config(config, db_type)
        
        # Setup migrations for SQL databases
        if db_type in ['postgresql', 'mysql', 'sqlite']:
            self._setup_migrations(db_type)
        
        # Store database config for later use
        self.db_config = config
        self.db_type = db_type
    
    def _update_database_config(self, config, db_type):
        """Update database configuration in framework-specific files"""
        app_dir = self.project_path / 'app'
        
        # Update config.py files based on framework
        if self.template_type == 'fastapi':
            config_file = app_dir / 'core' / 'config.py'
            if config_file.exists():
                content = config_file.read_text()
                # Replace DATABASE_URL line
                import re
                content = re.sub(
                    r'DATABASE_URL: str = ".*"',
                    f'DATABASE_URL: str = "{config["url"]}"',
                    content
                )
                config_file.write_text(content)
                
            # Update database.py
            db_file = app_dir / 'core' / 'database.py'
            if db_file.exists():
                if db_type == 'mongodb':
                    db_content = '''from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def get_database():
    return db.client[settings.DATABASE_URL.split('/')[-1]]
'''
                elif db_type == 'redis':
                    db_content = '''import redis.asyncio as redis
from app.core.config import settings

redis_client = None

async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = await redis.from_url(settings.DATABASE_URL)
    return redis_client
'''
                else:
                    # SQL databases
                    db_content = '''from sqlalchemy import create_engine
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
'''
                db_file.write_text(db_content)
        
        elif self.template_type == 'django':
            settings_file = self.project_path / 'config' / 'settings.py'
            if settings_file.exists():
                content = settings_file.read_text()
                # Update DATABASES configuration
                if db_type == 'mongodb':
                    # Django doesn't natively support MongoDB, but we can add djongo
                    pass
                elif db_type == 'redis':
                    # Redis is typically used for caching in Django
                    pass
                else:
                    # SQL databases
                    import re
                    content = re.sub(
                        r"env\.db\('DATABASE_URL', default='.*'\)",
                        f"env.db('DATABASE_URL', default='{config['url']}')",
                        content
                    )
                    settings_file.write_text(content)
        
        elif self.template_type == 'flask':
            config_file = app_dir / 'config.py'
            if config_file.exists():
                content = config_file.read_text()
                import re
                # Match single or multi-line SQLALCHEMY_DATABASE_URI assignment
                db_url = config['url']
                replacement = f"SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \\\n        '{db_url}'"
                content = re.sub(
                    r"SQLALCHEMY_DATABASE_URI = os\.environ\.get\('DATABASE_URL'\)\s+or\s+\\?\s*'[^']*'",
                    replacement,
                    content,
                    flags=re.MULTILINE
                )
                config_file.write_text(content)
        
        # For other frameworks, update config.py if it exists
        config_file = app_dir / 'config.py'
        if config_file.exists() and self.template_type not in ['fastapi', 'django', 'flask']:
            content = config_file.read_text()
            import re
            content = re.sub(
                r"DATABASE_URL = os\.getenv\('DATABASE_URL', '.*'\)",
                f"DATABASE_URL = os.getenv('DATABASE_URL', '{config['url']}')",
                content
            )
            config_file.write_text(content)
    
    def _setup_migrations(self, db_type):
        """Setup database migrations (Alembic for SQL databases)"""
        if self.template_type == 'fastapi':
            # FastAPI uses Alembic
            alembic_dir = self.project_path / 'alembic'
            alembic_dir.mkdir(exist_ok=True)
            (alembic_dir / '__init__.py').write_text('')
            
            versions_dir = alembic_dir / 'versions'
            versions_dir.mkdir(exist_ok=True)
            (versions_dir / '__init__.py').write_text('')
            
            # Create alembic.ini
            alembic_ini = '''[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
'''
            (self.project_path / 'alembic.ini').write_text(alembic_ini)
            
            # Create env.py
            env_py = '''from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings
from app.core.database import Base

# this is the Alembic Config object
config = context.config

# Set sqlalchemy.url from settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'''
            (alembic_dir / 'env.py').write_text(env_py)
            
            # Create script.py.mako template
            script_mako = '''"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
'''
            (alembic_dir / 'script.py.mako').write_text(script_mako)
        
        elif self.template_type == 'django':
            # Django has built-in migrations, no additional setup needed
            pass
        
        elif self.template_type == 'flask':
            # Flask uses Flask-Migrate which is already in dependencies
            # Migration setup is done via Flask CLI commands
            pass
        
        # For other frameworks, they can use Alembic if needed
        # We'll add basic Alembic setup for Pyramid, Tornado, etc. if SQL databases are used
    
    def _setup_authentication(self):
        """Setup authentication based on selected auth type"""
        auth_type = self.auth.lower()
        
        if auth_type == 'jwt':
            self._setup_jwt_auth()
        elif auth_type == 'oauth2':
            self._setup_oauth2_auth()
        elif auth_type == 'apikey':
            self._setup_apikey_auth()
        elif auth_type == 'basic':
            self._setup_basic_auth()
    
    def _setup_jwt_auth(self):
        """Setup JWT authentication"""
        app_dir = self.project_path / 'app'
        
        # Create auth directory
        auth_dir = app_dir / 'auth'
        auth_dir.mkdir(exist_ok=True)
        (auth_dir / '__init__.py').write_text('')
        
        # Create JWT utilities
        jwt_utils = '''from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """Decode and verify a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
'''
        (auth_dir / 'jwt_utils.py').write_text(jwt_utils)
        
        # Create dependencies/decorators based on framework
        if self.template_type == 'fastapi':
            dependencies = '''from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.auth.jwt_utils import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current authenticated user from JWT token"""
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Return user based on payload
    # Replace with your actual user retrieval logic
    return {"user_id": payload.get("sub")}
'''
            (auth_dir / 'dependencies.py').write_text(dependencies)
            
            # Create auth endpoints
            auth_endpoints = '''from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.jwt_utils import verify_password, get_password_hash, create_access_token
from app.auth.dependencies import get_current_user
from datetime import timedelta
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register")
async def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    # user = db.query(User).filter(User.email == email).first()
    # if user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    # hashed_password = get_password_hash(password)
    # new_user = User(username=username, email=email, hashed_password=hashed_password)
    # db.add(new_user)
    # db.commit()
    
    return {"message": "User registered successfully"}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get access token"""
    # Verify user credentials
    # user = db.query(User).filter(User.email == form_data.username).first()
    # if not user or not verify_password(form_data.password, user.hashed_password):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect email or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return current_user
'''
            auth_endpoints_dir = app_dir / 'api' / 'v1' / 'endpoints'
            auth_endpoints_dir.mkdir(parents=True, exist_ok=True)
            (auth_endpoints_dir / 'auth.py').write_text(auth_endpoints)
            
            # Update router to include auth
            router_file = app_dir / 'api' / 'v1' / 'router.py'
            if router_file.exists():
                content = router_file.read_text()
                if 'from app.api.v1.endpoints import auth' not in content:
                    content = content.replace(
                        'from app.api.v1.endpoints import items',
                        'from app.api.v1.endpoints import items, auth'
                    )
                    content = content.replace(
                        'api_router.include_router(items.router',
                        'api_router.include_router(auth.router)\napi_router.include_router(items.router'
                    )
                    router_file.write_text(content)
            
        elif self.template_type == 'django':
            # Django JWT setup
            serializers = '''from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
'''
            serializers_dir = self.project_path / 'apps' / 'core'
            serializers_dir.mkdir(parents=True, exist_ok=True)
            (serializers_dir / 'serializers.py').write_text(serializers)
            
            auth_views = '''from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from apps.core.serializers import UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login and get JWT tokens"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
'''
            views_file = serializers_dir / 'views.py'
            if views_file.exists():
                with open(views_file, 'a') as f:
                    f.write('\n\n' + auth_views)
            else:
                views_file.write_text(auth_views)
            
            # Update URLs to include auth endpoints
            urls_file = serializers_dir / 'urls.py'
            if urls_file.exists():
                content = urls_file.read_text()
                if 'auth' not in content:
                    content = content.replace(
                        'from . import views',
                        'from . import views\nfrom rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView'
                    )
                    content = content.replace(
                        'urlpatterns = [',
                        'urlpatterns = [\n    path("auth/register/", views.register, name="register"),\n    path("auth/login/", views.login, name="login"),\n    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),\n    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),'
                    )
                    urls_file.write_text(content)
            
            # Update Django settings to include JWT authentication
            settings_file = self.project_path / 'config' / 'settings.py'
            if settings_file.exists():
                content = settings_file.read_text()
                if 'REST_FRAMEWORK' in content and 'SIMPLE_JWT' not in content:
                    # Add JWT settings
                    jwt_settings = '''
# JWT Authentication
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}
'''
                    content = content.replace(
                        'REST_FRAMEWORK = {',
                        jwt_settings + '\nREST_FRAMEWORK = {'
                    )
                    settings_file.write_text(content)
        
        elif self.template_type == 'flask':
            # Flask JWT setup
            auth_blueprint = '''from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.auth.jwt_utils import verify_password, get_password_hash
from app import db
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    # username = data.get('username')
    # email = data.get('email')
    # password = data.get('password')
    
    # Create user logic here
    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login and get access token"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Verify credentials
    # user = User.query.filter_by(username=username).first()
    # if not user or not verify_password(password, user.hashed_password):
    #     return jsonify({"error": "Invalid credentials"}), 401
    
    # Create token
    access_token = create_access_token(
        identity=username,
        expires_delta=timedelta(minutes=30)
    )
    return jsonify({"access_token": access_token, "token_type": "bearer"})


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    current_user = get_jwt_identity()
    return jsonify({"user": current_user})
'''
            (auth_dir / 'routes.py').write_text(auth_blueprint)
            
            # Register auth blueprint in app factory
            init_file = app_dir / '__init__.py'
            if init_file.exists():
                content = init_file.read_text()
                if 'from app.auth.routes import auth_bp' not in content:
                    content = content.replace(
                        '    # Register blueprints',
                        '    # Register blueprints\n    from app.auth.routes import auth_bp\n    app.register_blueprint(auth_bp, url_prefix="/auth")'
                    )
                    init_file.write_text(content)
        
        # Update .env.example with JWT secret
        env_example = self.project_path / '.env.example'
        if env_example.exists():
            content = env_example.read_text()
            if 'JWT_SECRET_KEY' not in content:
                content += '\n# JWT Authentication\nJWT_SECRET_KEY=your-jwt-secret-key-here\nJWT_ALGORITHM=HS256\nJWT_ACCESS_TOKEN_EXPIRE_MINUTES=30\n'
                env_example.write_text(content)
    
    def _setup_oauth2_auth(self):
        """Setup OAuth2 authentication (Google, GitHub)"""
        app_dir = self.project_path / 'app'
        auth_dir = app_dir / 'auth'
        auth_dir.mkdir(exist_ok=True)
        (auth_dir / '__init__.py').write_text('')
        
        oauth2_config = '''# OAuth2 Configuration
# Install: pip install authlib

from authlib.integrations.requests_client import OAuth2Session
from app.core.config import settings

# Google OAuth2
GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/google/callback"

# GitHub OAuth2
GITHUB_CLIENT_ID = settings.GITHUB_CLIENT_ID
GITHUB_CLIENT_SECRET = settings.GITHUB_CLIENT_SECRET
GITHUB_REDIRECT_URI = "http://localhost:8000/auth/github/callback"
'''
        (auth_dir / 'oauth2_config.py').write_text(oauth2_config)
        
        if self.template_type == 'fastapi':
            oauth2_endpoints = '''from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2
from authlib.integrations.starlette_client import OAuth

router = APIRouter(prefix="/auth", tags=["oauth2"])

oauth = OAuth()

# Register OAuth providers
oauth.register(
    name="google",
    client_id="your-google-client-id",
    client_secret="your-google-client-secret",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

oauth.register(
    name="github",
    client_id="your-github-client-id",
    client_secret="your-github-client-secret",
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    access_token_url="https://github.com/login/oauth/access_token",
    client_kwargs={"scope": "user:email"},
)


@router.get("/google/login")
async def google_login():
    """Initiate Google OAuth login"""
    redirect_uri = "http://localhost:8000/auth/google/callback"
    return await oauth.google.authorize_redirect(redirect_uri)


@router.get("/google/callback")
async def google_callback(request):
    """Handle Google OAuth callback"""
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    # Create or update user in database
    return {"user": user_info}


@router.get("/github/login")
async def github_login():
    """Initiate GitHub OAuth login"""
    redirect_uri = "http://localhost:8000/auth/github/callback"
    return await oauth.github.authorize_redirect(redirect_uri)


@router.get("/github/callback")
async def github_callback(request):
    """Handle GitHub OAuth callback"""
    token = await oauth.github.authorize_access_token(request)
    # Fetch user info from GitHub API
    # Create or update user in database
    return {"message": "GitHub OAuth callback"}
'''
            auth_endpoints_dir = app_dir / 'api' / 'v1' / 'endpoints'
            auth_endpoints_dir.mkdir(parents=True, exist_ok=True)
            (auth_endpoints_dir / 'oauth2.py').write_text(oauth2_endpoints)
        
        # Update .env.example
        env_example = self.project_path / '.env.example'
        if env_example.exists():
            content = env_example.read_text()
            if 'GOOGLE_CLIENT_ID' not in content:
                content += '\n# OAuth2\nGOOGLE_CLIENT_ID=your-google-client-id\nGOOGLE_CLIENT_SECRET=your-google-client-secret\nGITHUB_CLIENT_ID=your-github-client-id\nGITHUB_CLIENT_SECRET=your-github-client-secret\n'
                env_example.write_text(content)
    
    def _setup_apikey_auth(self):
        """Setup API Key authentication"""
        app_dir = self.project_path / 'app'
        auth_dir = app_dir / 'auth'
        auth_dir.mkdir(exist_ok=True)
        (auth_dir / '__init__.py').write_text('')
        
        if self.template_type == 'fastapi':
            apikey_auth = '''from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import settings

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

VALID_API_KEYS = [settings.API_KEY]  # In production, store in database


async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify API key"""
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key
'''
            (auth_dir / 'apikey_auth.py').write_text(apikey_auth)
        
        elif self.template_type == 'flask':
            apikey_auth = '''from functools import wraps
from flask import request, jsonify
from app.core.config import Config

VALID_API_KEYS = [Config.API_KEY]  # In production, store in database


def require_api_key(f):
    """Decorator to require API key"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key not in VALID_API_KEYS:
            return jsonify({"error": "Invalid API Key"}), 403
        return f(*args, **kwargs)
    return decorated_function
'''
            (auth_dir / 'apikey_auth.py').write_text(apikey_auth)
        
        # Update .env.example
        env_example = self.project_path / '.env.example'
        if env_example.exists():
            content = env_example.read_text()
            if 'API_KEY' not in content:
                content += '\n# API Key Authentication\nAPI_KEY=your-api-key-here\n'
                env_example.write_text(content)
    
    def _setup_basic_auth(self):
        """Setup Basic Authentication"""
        app_dir = self.project_path / 'app'
        auth_dir = app_dir / 'auth'
        auth_dir.mkdir(parents=True, exist_ok=True)
        (auth_dir / '__init__.py').write_text('')
        
        if self.template_type == 'fastapi':
            basic_auth = '''from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.core.config import settings

security = HTTPBasic()

# In production, verify against database
VALID_USERS = {
    "admin": "admin123",
    "user": "user123"
}


def verify_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify basic authentication credentials"""
    password = VALID_USERS.get(credentials.username)
    if password is None or password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
'''
            (auth_dir / 'basic_auth.py').write_text(basic_auth)
        
        elif self.template_type == 'flask':
            basic_auth = '''from functools import wraps
from flask import request, Response
from werkzeug.security import check_password_hash

# In production, verify against database
VALID_USERS = {
    "admin": "pbkdf2:sha256:...",  # Hashed password
}


def check_auth(username, password):
    """Check username and password"""
    return username in VALID_USERS and check_password_hash(VALID_USERS[username], password)


def authenticate():
    """Send 401 response"""
    return Response(
        'Could not verify your access level for that URL.\\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(f):
    """Decorator to require basic auth"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
'''
            (auth_dir / 'basic_auth.py').write_text(basic_auth)
    
    def _create_common_files(self):
        """Create common files like .gitignore, README, etc."""
        # Get database config for docker-compose and .env
        db_config = getattr(self, 'db_config', None)
        db_type = getattr(self, 'db_type', 'postgresql')
        
        # Generate docker-compose.yml with database service (skip for minimal)
        docker_compose_content = ''
        if self.style != 'minimal':
            docker_compose_content = self._generate_docker_compose(db_config, db_type)
        
        # Generate .env.example with database URL (skip for minimal)
        env_example_content = ''
        if self.style != 'minimal':
            env_example_content = self._generate_env_example(db_config, db_type)
        else:
            # Minimal style: simple .env.example
            env_example_content = '''# Environment
DEBUG=True
SECRET_KEY=your-secret-key-here
'''
        
        context = {
            'project_name': self.project_name,
            'description': self.description,
            'author': self.author,
            'run_command': self._get_run_command(),
            'project_structure': self._get_project_structure(),
            'api_docs_info': self._get_api_docs_info(),
            'docker_cmd': self._get_docker_cmd(),
            'port': self._get_default_port(),
            'database_url': db_config['url'] if db_config else 'postgresql://user:password@localhost:5432/dbname',
            'database_type': db_type.upper() if db_config else 'SQLITE',
            'docker_compose': docker_compose_content,
            'env_example': env_example_content,
            'style': self.style
        }
        
        # Files to skip based on style
        skip_files = []
        if self.style == 'minimal':
            skip_files = ['Dockerfile', 'docker-compose.yml', 'pytest.ini']
        
        for filename, content in COMMON_FILES.items():
            # Skip certain files for minimal style
            if filename in skip_files:
                continue
            
            template = Template(content)
            rendered = template.render(**context)
            
            # Override docker-compose.yml and .env.example with database-specific versions
            if filename == 'docker-compose.yml' and docker_compose_content:
                rendered = docker_compose_content
            elif filename == '.env.example' and env_example_content:
                rendered = env_example_content
            elif filename == 'README.md':
                # Update README based on style
                rendered = self._generate_readme(context)
            
            (self.project_path / filename).write_text(rendered)
        
        # Add extra files for full style
        if self.style == 'full':
            self._add_full_style_files()
    
    def _generate_readme(self, context):
        """Generate README based on style"""
        if self.style == 'minimal':
            return f'''# {context['project_name']}

{context['description']}

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
{context['run_command']}
```

## Author

{context['author']}
'''
        else:
            # Use the standard README from COMMON_FILES
            template = Template(COMMON_FILES['README.md'])
            readme_content = template.render(**context)
            
            # Add authentication section if auth is enabled
            if self.auth:
                auth_section = self._generate_auth_readme_section()
                # Insert auth section before "## Author" section
                if '## Author' in readme_content:
                    readme_content = readme_content.replace('## Author', auth_section + '\n\n## Author')
                else:
                    readme_content += '\n\n' + auth_section
            
            return readme_content
    
    def _generate_auth_readme_section(self):
        """Generate authentication section for README"""
        auth_type = self.auth.lower()
        
        if auth_type == 'jwt':
            return '''## Authentication

This project uses JWT (JSON Web Tokens) for authentication.

### Endpoints

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token
- `GET /auth/me` - Get current user information (requires authentication)

### Usage Examples

#### Register a new user
```bash
curl -X POST "http://localhost:8000/auth/register" \\
  -H "Content-Type: application/json" \\
  -d '{"username": "user", "email": "user@example.com", "password": "password123"}'
```

#### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \\
  -H "Content-Type: application/x-www-form-urlencoded" \\
  -d "username=user&password=password123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Access protected endpoint
```bash
curl -X GET "http://localhost:8000/auth/me" \\
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Environment Variables

Update `.env` file with:
```
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```
'''
        
        elif auth_type == 'oauth2':
            return '''## Authentication

This project uses OAuth2 for authentication (Google, GitHub).

### OAuth2 Providers

- Google OAuth2
- GitHub OAuth2

### Usage Examples

#### Google OAuth2 Login
Visit: `http://localhost:8000/auth/google/login`

#### GitHub OAuth2 Login
Visit: `http://localhost:8000/auth/github/login`

### Environment Variables

Update `.env` file with:
```
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```
'''
        
        elif auth_type == 'apikey':
            return '''## Authentication

This project uses API Key authentication.

### Usage Examples

#### Access protected endpoint with API Key
```bash
curl -X GET "http://localhost:8000/api/items" \\
  -H "X-API-Key: your-api-key-here"
```

### Environment Variables

Update `.env` file with:
```
API_KEY=your-api-key-here
```

**Note:** In production, store API keys in a database and verify them properly.
'''
        
        elif auth_type == 'basic':
            return '''## Authentication

This project uses Basic Authentication.

### Usage Examples

#### Access protected endpoint with Basic Auth
```bash
curl -X GET "http://localhost:8000/api/items" \\
  -u username:password
```

Or with explicit header:
```bash
curl -X GET "http://localhost:8000/api/items" \\
  -H "Authorization: Basic $(echo -n 'username:password' | base64)"
```

**Note:** In production, verify credentials against a database and use HTTPS.
'''
        
        return ''
    
    def _add_full_style_files(self):
        """Add additional files for full style"""
        # .pre-commit-config.yaml placeholder
        pre_commit_config = '''# Pre-commit hooks configuration
# Install pre-commit: pip install pre-commit
# Then run: pre-commit install

repos:
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
'''
        (self.project_path / '.pre-commit-config.yaml').write_text(pre_commit_config)
        
        # pyproject.toml for tool configuration
        pyproject_toml = '''[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']

[tool.isort]
profile = "black"
line_length = 88

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["app"]
omit = ["*/tests/*", "*/__pycache__/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
'''
        (self.project_path / 'pyproject.toml').write_text(pyproject_toml)
        
        # .github/workflows/ci.yml placeholder
        workflows_dir = self.project_path / '.github' / 'workflows'
        workflows_dir.mkdir(parents=True)
        
        ci_workflow = '''name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest
    
    - name: Run linting
      run: |
        black --check .
        flake8 .
        isort --check-only .
'''
        (workflows_dir / 'ci.yml').write_text(ci_workflow)
        
        # Makefile for convenience
        makefile_content = f'''.PHONY: install test run docker-build docker-up clean lint format migrate

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest

test-cov:
	pytest --cov=app --cov-report=html --cov-report=term-missing

run:
	{self._get_run_command()}

docker-build:
	docker-compose build

docker-up:
	docker-compose up

docker-down:
	docker-compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {{}} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {{}} +

lint:
	black --check .
	flake8 .
	isort --check-only .

format:
	black .
	isort .

migrate:
	# Framework-specific migration command
	# FastAPI: alembic upgrade head
	# Django: python manage.py migrate
	# Flask: flask db upgrade

help:
	@echo "Available commands:"
	@echo "  make install     - Install dependencies"
	@echo "  make test        - Run tests"
	@echo "  make run         - Run development server"
	@echo "  make format      - Format code with black and isort"
	@echo "  make lint        - Check code formatting and linting"
	@echo "  make docker-up   - Start Docker containers"
	@echo "  make clean       - Remove Python cache files"
'''
        (self.project_path / 'Makefile').write_text(makefile_content)
    
    def _generate_docker_compose(self, db_config, db_type):
        """Generate docker-compose.yml with appropriate database service"""
        port = self._get_default_port()
        
        if db_type == 'sqlite':
            # SQLite doesn't need a database service
            return f'''version: '3.8'

services:
  web:
    build: .
    ports:
      - "{port}:{port}"
    environment:
      - DATABASE_URL={db_config['docker_url'] if db_config else 'sqlite:///./app.db'}
      - DEBUG=True
    volumes:
      - .:/app
'''
        
        if not db_config or not db_config.get('docker_image'):
            # Default to PostgreSQL if no config
            db_config = {
                'docker_image': 'postgres:15',
                'docker_env': {
                    'POSTGRES_DB': 'appdb',
                    'POSTGRES_USER': 'postgres',
                    'POSTGRES_PASSWORD': 'postgres'
                },
                'docker_url': 'postgresql://postgres:postgres@db:5432/appdb'
            }
        
        # Build environment variables string
        env_vars = [f"      - DATABASE_URL={db_config['docker_url']}", "      - DEBUG=True"]
        db_env_vars = '\n'.join([f"      - {k}={v}" for k, v in db_config['docker_env'].items()])
        
        return f'''version: '3.8'

services:
  web:
    build: .
    ports:
      - "{port}:{port}"
    environment:
{chr(10).join(env_vars)}
    depends_on:
      - db
    volumes:
      - .:/app

  db:
    image: {db_config['docker_image']}
{db_env_vars}
    volumes:
      - {db_type}_data:/var/lib/{db_type}/data

volumes:
  {db_type}_data:
'''
    
    def _generate_env_example(self, db_config, db_type):
        """Generate .env.example with database URL"""
        db_url = db_config['url'] if db_config else 'postgresql://user:password@localhost:5432/dbname'
        
        return f'''# Database
DATABASE_URL={db_url}

# Security
SECRET_KEY=your-secret-key-here

# Environment
DEBUG=True
ENVIRONMENT=development
PORT={self._get_default_port()}
'''
    
    def _create_requirements(self):
        """Create requirements.txt and requirements-dev.txt"""
        deps = self.template_config['dependencies'].copy()
        dev_deps = self.template_config['dev_dependencies']
        
        # Add database-specific packages (skip for minimal style)
        if self.style != 'minimal' and hasattr(self, 'db_config') and self.db_config.get('packages'):
            # Remove existing database packages from deps to avoid duplicates
            db_packages_to_remove = ['psycopg2-binary', 'pymysql', 'motor', 'pymongo', 'redis', 'hiredis']
            deps = [d for d in deps if not any(pkg in d for pkg in db_packages_to_remove)]
            
            # Add new database packages
            deps.extend(self.db_config['packages'])
        
        # Add authentication packages
        if self.auth:
            auth_packages = self._get_auth_packages()
            # Remove existing auth packages to avoid duplicates
            auth_packages_to_remove = ['python-jose', 'passlib', 'bcrypt', 'authlib', 'flask-jwt-extended', 'djangorestframework-simplejwt']
            deps = [d for d in deps if not any(pkg in d for pkg in auth_packages_to_remove)]
            deps.extend(auth_packages)
        
        (self.project_path / 'requirements.txt').write_text('\n'.join(deps))
        
        # Skip dev dependencies for minimal style
        if self.style != 'minimal':
            (self.project_path / 'requirements-dev.txt').write_text(
                '-r requirements.txt\n' + '\n'.join(dev_deps)
            )
    
    def _get_auth_packages(self):
        """Get authentication packages based on auth type and framework"""
        auth_type = self.auth.lower()
        packages = []
        
        if auth_type == 'jwt':
            if self.template_type == 'django':
                packages = ['djangorestframework-simplejwt>=5.3.0']
            elif self.template_type == 'flask':
                packages = ['flask-jwt-extended>=4.5.3', 'python-jose[cryptography]>=3.3.0', 'passlib[bcrypt]>=1.7.4']
            else:
                packages = ['python-jose[cryptography]>=3.3.0', 'passlib[bcrypt]>=1.7.4']
        
        elif auth_type == 'oauth2':
            packages = ['authlib>=1.2.1']
        
        elif auth_type == 'apikey':
            # API Key doesn't require additional packages
            pass
        
        elif auth_type == 'basic':
            if self.template_type == 'flask':
                # werkzeug is already in Flask dependencies
                packages = ['passlib[bcrypt]>=1.7.4']
            else:
                packages = ['passlib[bcrypt]>=1.7.4']
        
        return packages
    
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
            'flask': 'python run.py',
            'bottle': 'python app/main.py',
            'pyramid': 'python run.py',
            'tornado': 'python app/main.py',
            'sanic': 'python app/main.py',
            'cherrypy': 'python app/main.py'
        }
        return commands.get(self.template_type, '')
    
    def _get_project_structure(self):
        structures = {
            'fastapi': 'app/\n├── main.py\n├── core/\n├── api/\n├── models/\n└── schemas/',
            'django': 'config/\napps/\n├── core/\nmanage.py',
            'flask': 'app/\n├── __init__.py\n├── api/\n├── models/\nrun.py',
            'bottle': 'app/\n├── main.py\n├── config.py\n├── routes/\n└── models/',
            'pyramid': 'app/\n├── main.py\n├── config.py\n├── routes/\n├── models/\nrun.py',
            'tornado': 'app/\n├── main.py\n├── config.py\n├── routes/\n└── models/',
            'sanic': 'app/\n├── main.py\n├── config.py\n├── routes/\n└── models/',
            'cherrypy': 'app/\n├── main.py\n├── config.py\n├── routes/\n└── models/'
        }
        return structures.get(self.template_type, '')
    
    def _get_api_docs_info(self):
        docs = {
            'fastapi': 'Visit http://localhost:8000/docs for Swagger UI',
            'django': 'API endpoints available at /api/',
            'flask': 'API endpoints available at /api/',
            'bottle': 'API endpoints available at /api/',
            'pyramid': 'API endpoints available at /api/',
            'tornado': 'API endpoints available at /api/',
            'sanic': 'Visit http://localhost:8000/docs for API documentation',
            'cherrypy': 'API endpoints available at /api/'
        }
        return docs.get(self.template_type, '')
    
    def _get_docker_cmd(self):
        cmds = {
            'fastapi': 'CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]',
            'django': 'CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]',
            'flask': 'CMD ["python", "run.py"]',
            'bottle': 'CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app.main:app"]',
            'pyramid': 'CMD ["waitress-serve", "--host=0.0.0.0", "--port=8000", "app.main:main"]',
            'tornado': 'CMD ["python", "app/main.py"]',
            'sanic': 'CMD ["sanic", "app.main.app", "--host=0.0.0.0", "--port=8000"]',
            'cherrypy': 'CMD ["python", "app/main.py"]'
        }
        return cmds.get(self.template_type, '')
    
    def _get_default_port(self):
        ports = {
            'fastapi': '8000',
            'django': '8000',
            'flask': '5000',
            'bottle': '8000',
            'pyramid': '8000',
            'tornado': '8000',
            'sanic': '8000',
            'cherrypy': '8000'
        }
        return ports.get(self.template_type, '8000')

    def _validate_generation(self) -> None:
        """Lightweight sanity checks to ensure the generated project is runnable."""
        try:
            # Common checks
            assert (self.project_path / 'requirements.txt').exists(), 'requirements.txt missing'
            # Template specific entry files
            entrypoints = {
                'fastapi': self.project_path / 'app' / 'main.py',
                'flask': self.project_path / 'run.py',
                'django': self.project_path / 'manage.py',
                'bottle': self.project_path / 'app' / 'main.py',
                'pyramid': self.project_path / 'run.py',
                'tornado': self.project_path / 'app' / 'main.py',
                'sanic': self.project_path / 'app' / 'main.py',
                'cherrypy': self.project_path / 'app' / 'main.py',
            }
            entry = entrypoints.get(self.template_type)
            if entry is not None:
                assert entry.exists(), f'Entrypoint not found: {entry}'
        except AssertionError as e:
            # Surface a clear error to the CLI layer
            raise RuntimeError(f"Post-generation validation failed: {e}")