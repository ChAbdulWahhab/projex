"""Framework detection utilities"""
from pathlib import Path
from typing import Optional


def detect_framework(project_path: Path) -> Optional[str]:
    """
    Detect which framework is being used in the project.
    
    Args:
        project_path: Path to the project root
        
    Returns:
        Framework name (fastapi, django, flask, etc.) or None if not detected
    """
    # Check for FastAPI
    if (project_path / 'app' / 'main.py').exists():
        try:
            content = (project_path / 'app' / 'main.py').read_text()
            if 'from fastapi import' in content or 'import fastapi' in content:
                return 'fastapi'
        except:
            pass
    
    # Check for Django
    if (project_path / 'manage.py').exists():
        return 'django'
    
    # Check for Flask
    if (project_path / 'app' / '__init__.py').exists():
        try:
            content = (project_path / 'app' / '__init__.py').read_text()
            if 'from flask import' in content or 'import flask' in content:
                return 'flask'
        except:
            pass
    
    # Check for Bottle
    if (project_path / 'app' / 'main.py').exists():
        try:
            content = (project_path / 'app' / 'main.py').read_text()
            if 'from bottle import' in content or 'import bottle' in content:
                return 'bottle'
        except:
            pass
    
    # Check for Pyramid
    if (project_path / 'development.ini').exists() or (project_path / 'app' / 'main.py').exists():
        try:
            if (project_path / 'app' / 'main.py').exists():
                content = (project_path / 'app' / 'main.py').read_text()
                if 'from pyramid' in content or 'pyramid.config' in content:
                    return 'pyramid'
        except:
            pass
    
    # Check for Tornado
    if (project_path / 'app' / 'main.py').exists():
        try:
            content = (project_path / 'app' / 'main.py').read_text()
            if 'import tornado' in content or 'tornado.web' in content:
                return 'tornado'
        except:
            pass
    
    # Check for Sanic
    if (project_path / 'app' / 'main.py').exists():
        try:
            content = (project_path / 'app' / 'main.py').read_text()
            if 'from sanic import' in content or 'import sanic' in content:
                return 'sanic'
        except:
            pass
    
    # Check for CherryPy
    if (project_path / 'app' / 'main.py').exists():
        try:
            content = (project_path / 'app' / 'main.py').read_text()
            if 'import cherrypy' in content or 'cherrypy' in content:
                return 'cherrypy'
        except:
            pass
    
    return None

