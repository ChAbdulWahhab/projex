"""Gitignore generation utilities"""
import requests
from pathlib import Path
from typing import List


def generate_gitignore(project_path: Path, templates: List[str]) -> Path:
    """
    Generate .gitignore file using gitignore.io API.
    
    Args:
        project_path: Path to project root
        templates: List of gitignore templates (e.g., ['python', 'venv', 'pycharm'])
        
    Returns:
        Path to created .gitignore file
    """
    # Combine templates
    template_str = ','.join(templates)
    
    try:
        # Fetch from gitignore.io API
        url = f'https://www.toptal.com/developers/gitignore/api/{template_str}'
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            gitignore_content = response.text
        else:
            # Fallback to basic Python gitignore
            gitignore_content = _get_basic_python_gitignore()
    except Exception:
        # Fallback to basic Python gitignore
        gitignore_content = _get_basic_python_gitignore()
    
    # Add custom entries
    gitignore_content += """

# Custom additions
.env
.env.local
.env.*.local
*.log
.DS_Store
Thumbs.db
"""
    
    gitignore_file = project_path / '.gitignore'
    
    # Append if exists, otherwise create
    if gitignore_file.exists():
        existing = gitignore_file.read_text()
        # Only add if not already there
        if '# Custom additions' not in existing:
            gitignore_file.write_text(existing + gitignore_content)
    else:
        gitignore_file.write_text(gitignore_content)
    
    return gitignore_file


def _get_basic_python_gitignore() -> str:
    """Get basic Python gitignore template"""
    return """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
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
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/
"""

