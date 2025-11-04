"""Code generation utilities for scaffolding"""
from pathlib import Path
from typing import List, Tuple


# Field type mappings
TYPE_MAPPINGS = {
    'str': 'str',
    'int': 'int',
    'float': 'float',
    'bool': 'bool',
    'date': 'datetime.date',
    'datetime': 'datetime.datetime',
    'list': 'List',
    'dict': 'Dict',
}


def generate_model(framework: str, name: str, fields: List[Tuple[str, str]]) -> str:
    """Generate model code for a given framework"""
    model_name = name.capitalize()
    
    if framework == 'fastapi':
        return _generate_fastapi_model(model_name, fields)
    elif framework == 'django':
        return _generate_django_model(model_name, fields)
    elif framework == 'flask':
        return _generate_flask_model(model_name, fields)
    else:
        # Generic SQLAlchemy model for other frameworks
        return _generate_sqlalchemy_model(model_name, fields)


def _generate_fastapi_model(name: str, fields: List[Tuple[str, str]]) -> str:
    """Generate FastAPI/SQLAlchemy model"""
    imports = ['from sqlalchemy import Column, Integer, String, Boolean, DateTime']
    model_fields = []
    
    for field_name, field_type in fields:
        sqlalchemy_type = _get_sqlalchemy_type(field_type)
        if field_name == 'id':
            model_fields.append(f"    id = Column(Integer, primary_key=True, index=True)")
        else:
            model_fields.append(f"    {field_name} = Column({sqlalchemy_type})")
    
    if 'DateTime' in str(model_fields):
        imports.append('from datetime import datetime')
    
    model_code = f'''from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime

Base = declarative_base()


class {name}(Base):
    __tablename__ = "{name.lower()}s"
    
    id = Column(Integer, primary_key=True, index=True)
'''
    
    for field_name, field_type in fields:
        if field_name != 'id':
            sqlalchemy_type = _get_sqlalchemy_type(field_type)
            model_code += f"    {field_name} = Column({sqlalchemy_type})\n"
    
    return model_code


def _generate_django_model(name: str, fields: List[Tuple[str, str]]) -> str:
    """Generate Django model"""
    model_code = f'''from django.db import models


class {name}(models.Model):
'''
    
    for field_name, field_type in fields:
        if field_name == 'id':
            continue  # Django auto-creates id
        django_field = _get_django_field(field_type)
        model_code += f"    {field_name} = models.{django_field}\n"
    
    model_code += "\n    class Meta:\n        db_table = '{}s'\n        ordering = ['-id']\n".format(name.lower())
    model_code += f"\n    def __str__(self):\n        return f\"{name} {{self.id}}\"\n"
    
    return model_code


def _generate_flask_model(name: str, fields: List[Tuple[str, str]]) -> str:
    """Generate Flask-SQLAlchemy model"""
    model_code = f'''from app import db


class {name}(db.Model):
    __tablename__ = "{name.lower()}s"
    
    id = db.Column(db.Integer, primary_key=True)
'''
    
    for field_name, field_type in fields:
        if field_name != 'id':
            sqlalchemy_type = _get_sqlalchemy_type(field_type)
            model_code += f"    {field_name} = db.Column(db.{sqlalchemy_type})\n"
    
    model_code += f"\n    def __repr__(self):\n        return f\"<{name}(id={{self.id}})>\"\n"
    
    return model_code


def _generate_sqlalchemy_model(name: str, fields: List[Tuple[str, str]]) -> str:
    """Generate generic SQLAlchemy model"""
    return _generate_fastapi_model(name, fields)


def _get_sqlalchemy_type(python_type: str) -> str:
    """Map Python type to SQLAlchemy type"""
    mapping = {
        'str': 'String',
        'int': 'Integer',
        'float': 'Float',
        'bool': 'Boolean',
        'date': 'Date',
        'datetime': 'DateTime',
        'list': 'Text',  # Store as JSON string
        'dict': 'Text',  # Store as JSON string
    }
    return mapping.get(python_type.lower(), 'String')


def _get_django_field(python_type: str) -> str:
    """Map Python type to Django field"""
    mapping = {
        'str': 'CharField(max_length=255)',
        'int': 'IntegerField()',
        'float': 'FloatField()',
        'bool': 'BooleanField(default=False)',
        'date': 'DateField()',
        'datetime': 'DateTimeField(auto_now_add=True)',
        'list': 'JSONField(default=list)',
        'dict': 'JSONField(default=dict)',
    }
    return mapping.get(python_type.lower(), 'CharField(max_length=255)')


def save_model(framework: str, project_path: Path, name: str, code: str) -> Path:
    """Save model to appropriate location"""
    model_name = name.lower()
    
    if framework == 'django':
        # Django models go in apps
        models_dir = project_path / 'apps' / 'core' / 'models.py'
        if models_dir.exists():
            # Append to existing models.py
            with open(models_dir, 'a') as f:
                f.write('\n\n' + code)
            return models_dir
        else:
            # Create new models.py
            models_dir.parent.mkdir(parents=True, exist_ok=True)
            models_dir.write_text(code)
            return models_dir
    else:
        # Other frameworks: save to app/models/
        models_dir = project_path / 'app' / 'models'
        models_dir.mkdir(parents=True, exist_ok=True)
        model_file = models_dir / f'{model_name}.py'
        model_file.write_text(code)
        
        # Update __init__.py
        init_file = models_dir / '__init__.py'
        if init_file.exists():
            content = init_file.read_text()
            if f'from .{model_name} import' not in content:
                init_file.write_text(content + f'\nfrom .{model_name} import {name.capitalize()}\n')
        else:
            init_file.write_text(f'from .{model_name} import {name.capitalize()}\n')
        
        return model_file


def generate_endpoint(framework: str, name: str, crud: bool) -> str:
    """Generate endpoint/route code"""
    if framework == 'fastapi':
        return _generate_fastapi_endpoint(name, crud)
    elif framework == 'django':
        return _generate_django_endpoint(name, crud)
    elif framework == 'flask':
        return _generate_flask_endpoint(name, crud)
    else:
        return _generate_generic_endpoint(framework, name, crud)


def _generate_fastapi_endpoint(name: str, crud: bool) -> str:
    """Generate FastAPI endpoint"""
    endpoint_name = name.lower()
    model_name = name.capitalize()
    
    if crud:
        return f'''from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.{endpoint_name} import {model_name}
from app.schemas.{endpoint_name} import {model_name}Create, {model_name}Update, {model_name}Response

router = APIRouter(prefix="/{endpoint_name}s", tags=["{endpoint_name}s"])


@router.get("/", response_model=List[{model_name}Response])
async def get_{endpoint_name}s(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all {endpoint_name}s"""
    {endpoint_name}s = db.query({model_name}).offset(skip).limit(limit).all()
    return {endpoint_name}s


@router.get("/{{item_id}}", response_model={model_name}Response)
async def get_{endpoint_name}(item_id: int, db: Session = Depends(get_db)):
    """Get a single {endpoint_name}"""
    {endpoint_name} = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not {endpoint_name}:
        raise HTTPException(status_code=404, detail="{model_name} not found")
    return {endpoint_name}


@router.post("/", response_model={model_name}Response, status_code=201)
async def create_{endpoint_name}({endpoint_name}: {model_name}Create, db: Session = Depends(get_db)):
    """Create a new {endpoint_name}"""
    db_{endpoint_name} = {model_name}(**{endpoint_name}.dict())
    db.add(db_{endpoint_name})
    db.commit()
    db.refresh(db_{endpoint_name})
    return db_{endpoint_name}


@router.put("/{{item_id}}", response_model={model_name}Response)
async def update_{endpoint_name}(item_id: int, {endpoint_name}_update: {model_name}Update, db: Session = Depends(get_db)):
    """Update a {endpoint_name}"""
    db_{endpoint_name} = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not db_{endpoint_name}:
        raise HTTPException(status_code=404, detail="{model_name} not found")
    
    for key, value in {endpoint_name}_update.dict(exclude_unset=True).items():
        setattr(db_{endpoint_name}, key, value)
    
    db.commit()
    db.refresh(db_{endpoint_name})
    return db_{endpoint_name}


@router.delete("/{{item_id}}", status_code=204)
async def delete_{endpoint_name}(item_id: int, db: Session = Depends(get_db)):
    """Delete a {endpoint_name}"""
    db_{endpoint_name} = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not db_{endpoint_name}:
        raise HTTPException(status_code=404, detail="{model_name} not found")
    
    db.delete(db_{endpoint_name})
    db.commit()
    return None
'''
    else:
        return f'''from fastapi import APIRouter

router = APIRouter(prefix="/{endpoint_name}s", tags=["{endpoint_name}s"])


@router.get("/")
async def get_{endpoint_name}s():
    """Get all {endpoint_name}s"""
    return {{"message": "Get all {endpoint_name}s"}}


@router.get("/{{item_id}}")
async def get_{endpoint_name}(item_id: int):
    """Get a single {endpoint_name}"""
    return {{"message": f"Get {endpoint_name} {{item_id}}"}}
'''


def _generate_django_endpoint(name: str, crud: bool) -> str:
    """Generate Django REST Framework viewset"""
    endpoint_name = name.lower()
    model_name = name.capitalize()
    
    if crud:
        return f'''from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.core.models import {model_name}
from apps.core.serializers import {model_name}Serializer


class {model_name}ViewSet(viewsets.ModelViewSet):
    """
    ViewSet for {model_name} model
    Provides CRUD operations
    """
    queryset = {model_name}.objects.all()
    serializer_class = {model_name}Serializer
'''
    else:
        return f'''from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def {endpoint_name}_list(request):
    """List all {endpoint_name}s"""
    return Response({{"message": "List {endpoint_name}s"}})


@api_view(['GET'])
def {endpoint_name}_detail(request, pk):
    """Get a single {endpoint_name}"""
    return Response({{"message": f"Get {endpoint_name} {{pk}}"}})
'''


def _generate_flask_endpoint(name: str, crud: bool) -> str:
    """Generate Flask blueprint"""
    endpoint_name = name.lower()
    model_name = name.capitalize()
    
    if crud:
        bp_name = f'{endpoint_name}_bp'
        return f'''from flask import Blueprint, request, jsonify
from app.models.{endpoint_name} import {model_name}
from app import db

{bp_name} = Blueprint('{endpoint_name}', __name__)


@{bp_name}.route('/', methods=['GET'])
def get_{endpoint_name}s():
    """Get all {endpoint_name}s"""
    {endpoint_name}s = {model_name}.query.all()
    return jsonify([{{"id": item.id}} for item in {endpoint_name}s])


@{bp_name}.route('/<int:item_id>', methods=['GET'])
def get_{endpoint_name}(item_id):
    """Get a single {endpoint_name}"""
    {endpoint_name} = {model_name}.query.get_or_404(item_id)
    return jsonify({{"id": {endpoint_name}.id}})


@{bp_name}.route('/', methods=['POST'])
def create_{endpoint_name}():
    """Create a new {endpoint_name}"""
    data = request.get_json()
    {endpoint_name} = {model_name}(**data)
    db.session.add({endpoint_name})
    db.session.commit()
    return jsonify({{"id": {endpoint_name}.id}}), 201


@{bp_name}.route('/<int:item_id>', methods=['PUT'])
def update_{endpoint_name}(item_id):
    """Update a {endpoint_name}"""
    {endpoint_name} = {model_name}.query.get_or_404(item_id)
    data = request.get_json()
    for key, value in data.items():
        setattr({endpoint_name}, key, value)
    db.session.commit()
    return jsonify({{"id": {endpoint_name}.id}})


@{bp_name}.route('/<int:item_id>', methods=['DELETE'])
def delete_{endpoint_name}(item_id):
    """Delete a {endpoint_name}"""
    {endpoint_name} = {model_name}.query.get_or_404(item_id)
    db.session.delete({endpoint_name})
    db.session.commit()
    return '', 204
'''
    else:
        return f'''from flask import Blueprint, jsonify

{endpoint_name}_bp = Blueprint('{endpoint_name}', __name__)


@{endpoint_name}_bp.route('/')
def get_{endpoint_name}s():
    """Get all {endpoint_name}s"""
    return jsonify({{"message": "Get all {endpoint_name}s"}})


@{endpoint_name}_bp.route('/<int:item_id>')
def get_{endpoint_name}(item_id):
    """Get a single {endpoint_name}"""
    return jsonify({{"message": f"Get {endpoint_name} {{item_id}}"}})
'''


def _generate_generic_endpoint(framework: str, name: str, crud: bool) -> str:
    """Generate generic endpoint for other frameworks"""
    endpoint_name = name.lower()
    return f'''# {name.capitalize()} endpoint for {framework}
# Implement your endpoint logic here

def get_{endpoint_name}s():
    """Get all {endpoint_name}s"""
    return {{"message": "Get all {endpoint_name}s"}}


def get_{endpoint_name}(item_id):
    """Get a single {endpoint_name}"""
    return {{"message": f"Get {endpoint_name} {{item_id}}"}}
'''


def save_endpoint(framework: str, project_path: Path, name: str, code: str, crud: bool) -> Path:
    """Save endpoint to appropriate location"""
    endpoint_name = name.lower()
    
    if framework == 'fastapi':
        endpoints_dir = project_path / 'app' / 'api' / 'v1' / 'endpoints'
        endpoints_dir.mkdir(parents=True, exist_ok=True)
        endpoint_file = endpoints_dir / f'{endpoint_name}.py'
        endpoint_file.write_text(code)
        return endpoint_file
    elif framework == 'django':
        views_file = project_path / 'apps' / 'core' / 'views.py'
        if views_file.exists():
            with open(views_file, 'a') as f:
                f.write('\n\n' + code)
        else:
            views_file.parent.mkdir(parents=True, exist_ok=True)
            views_file.write_text(code)
        return views_file
    elif framework == 'flask':
        api_dir = project_path / 'app' / 'api'
        api_dir.mkdir(parents=True, exist_ok=True)
        endpoint_file = api_dir / f'{endpoint_name}.py'
        endpoint_file.write_text(code)
        return endpoint_file
    else:
        routes_dir = project_path / 'app' / 'routes'
        routes_dir.mkdir(parents=True, exist_ok=True)
        endpoint_file = routes_dir / f'{endpoint_name}.py'
        endpoint_file.write_text(code)
        return endpoint_file


def generate_service(framework: str, name: str, is_async: bool) -> str:
    """Generate service class"""
    service_name = name.capitalize()
    async_prefix = 'async ' if is_async else ''
    await_keyword = 'await ' if is_async else ''
    
    return f'''class {service_name}Service:
    """Service class for {name} operations"""
    
    def __init__(self):
        pass
    
    {async_prefix}def get_all(self):
        """Get all items"""
        # Implement your logic here
        return []
    
    {async_prefix}def get_by_id(self, item_id: int):
        """Get item by ID"""
        # Implement your logic here
        return None
    
    {async_prefix}def create(self, data: dict):
        """Create a new item"""
        # Implement your logic here
        return {{"id": 1, **data}}
    
    {async_prefix}def update(self, item_id: int, data: dict):
        """Update an item"""
        # Implement your logic here
        return {{"id": item_id, **data}}
    
    {async_prefix}def delete(self, item_id: int):
        """Delete an item"""
        # Implement your logic here
        return True
'''


def save_service(framework: str, project_path: Path, name: str, code: str) -> Path:
    """Save service to appropriate location"""
    service_name = name.lower()
    services_dir = project_path / 'app' / 'services'
    services_dir.mkdir(parents=True, exist_ok=True)
    service_file = services_dir / f'{service_name}_service.py'
    service_file.write_text(code)
    
    # Update __init__.py
    init_file = services_dir / '__init__.py'
    if init_file.exists():
        content = init_file.read_text()
        if f'from .{service_name}_service import' not in content:
            init_file.write_text(content + f'\nfrom .{service_name}_service import {name.capitalize()}Service\n')
    else:
        init_file.write_text(f'from .{service_name}_service import {name.capitalize()}Service\n')
    
    return service_file


def generate_middleware(framework: str, name: str) -> str:
    """Generate middleware code"""
    middleware_name = name.capitalize()
    
    if framework == 'fastapi':
        return f'''from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class {middleware_name}Middleware(BaseHTTPMiddleware):
    """{middleware_name} middleware"""
    
    async def dispatch(self, request: Request, call_next):
        # Add your middleware logic here
        # Before request
        response = await call_next(request)
        # After request
        return response
'''
    elif framework == 'django':
        return f'''class {middleware_name}Middleware:
    """{middleware_name} middleware"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Code to execute before view
        response = self.get_response(request)
        # Code to execute after view
        return response
'''
    elif framework == 'flask':
        return f'''from flask import request, g


class {middleware_name}Middleware:
    """{middleware_name} middleware"""
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    def before_request(self):
        # Code to execute before request
        pass
    
    def after_request(self, response):
        # Code to execute after request
        return response
'''
    else:
        return f'''# {middleware_name} Middleware for {framework}
# Implement your middleware logic here

class {middleware_name}Middleware:
    """{middleware_name} middleware"""
    
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        # Add your middleware logic here
        return self.app(environ, start_response)
'''


def save_middleware(framework: str, project_path: Path, name: str, code: str) -> Path:
    """Save middleware to appropriate location"""
    middleware_name = name.lower()
    middleware_dir = project_path / 'app' / 'middleware'
    middleware_dir.mkdir(parents=True, exist_ok=True)
    middleware_file = middleware_dir / f'{middleware_name}.py'
    middleware_file.write_text(code)
    
    # Update __init__.py
    init_file = middleware_dir / '__init__.py'
    if init_file.exists():
        content = init_file.read_text()
        if f'from .{middleware_name} import' not in content:
            init_file.write_text(content + f'\nfrom .{middleware_name} import {name.capitalize()}Middleware\n')
    else:
        init_file.write_text(f'from .{middleware_name} import {name.capitalize()}Middleware\n')
    
    return middleware_file

