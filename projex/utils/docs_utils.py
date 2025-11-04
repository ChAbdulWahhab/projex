"""Documentation generation utilities"""
from pathlib import Path
from typing import Optional


def generate_mkdocs(project_path: Path, framework: Optional[str] = None) -> Path:
    """
    Generate MkDocs documentation setup.
    
    Args:
        project_path: Path to project root
        framework: Detected framework name
        
    Returns:
        Path to created mkdocs.yml
    """
    docs_dir = project_path / 'docs'
    docs_dir.mkdir(exist_ok=True)
    
    # Create mkdocs.yml
    mkdocs_content = """site_name: {{ project_name }} Documentation
site_description: API documentation generated with Projex
site_author: Developer

theme:
  name: material
  palette:
    - scheme: default
      primary: blue
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: blue
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.annotate

nav:
  - Home: index.md
  - Getting Started:
    - Installation: setup/installation.md
    - Configuration: setup/configuration.md
  - API Reference:
    - Overview: api/overview.md
    - Endpoints: api/endpoints.md
  - Development:
    - Contributing: development/contributing.md
    - Testing: development/testing.md

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format

plugins:
  - search
"""
    
    # Replace placeholder if project name available
    try:
        project_name = project_path.name
        mkdocs_content = mkdocs_content.replace('{{ project_name }}', project_name)
    except:
        pass
    
    mkdocs_file = project_path / 'mkdocs.yml'
    mkdocs_file.write_text(mkdocs_content)
    
    # Create documentation files
    _create_mkdocs_files(docs_dir, framework)
    
    return mkdocs_file


def _create_mkdocs_files(docs_dir: Path, framework: Optional[str] = None):
    """Create initial MkDocs documentation files"""
    
    # index.md
    index_content = """# Welcome

Welcome to the API documentation!

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
# Add your run command here
```

## Features

- Fast and modern
- Well documented
- Easy to extend

## Getting Help

Check out the [Getting Started](setup/installation.md) guide for more information.
"""
    (docs_dir / 'index.md').write_text(index_content)
    
    # Setup directory
    setup_dir = docs_dir / 'setup'
    setup_dir.mkdir(exist_ok=True)
    
    # installation.md
    install_content = """# Installation

## Requirements

- Python 3.8+
- pip

## Install from Source

```bash
git clone <repository-url>
cd <project-name>
pip install -r requirements.txt
```

## Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```
"""
    (setup_dir / 'installation.md').write_text(install_content)
    
    # configuration.md
    config_content = """# Configuration

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

## Key Settings

- `DEBUG`: Enable debug mode
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Application secret key
"""
    (setup_dir / 'configuration.md').write_text(config_content)
    
    # API directory
    api_dir = docs_dir / 'api'
    api_dir.mkdir(exist_ok=True)
    
    # overview.md
    overview_content = """# API Overview

This API provides endpoints for various operations.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Most endpoints require authentication. Include your API key in the header:

```
Authorization: Bearer <your-token>
```
"""
    (api_dir / 'overview.md').write_text(overview_content)
    
    # endpoints.md
    endpoints_content = """# API Endpoints

## Health Check

```http
GET /health
```

Returns the health status of the API.

### Response

```json
{
  "status": "healthy"
}
```
"""
    (api_dir / 'endpoints.md').write_text(endpoints_content)
    
    # Development directory
    dev_dir = docs_dir / 'development'
    dev_dir.mkdir(exist_ok=True)
    
    # contributing.md
    contrib_content = """# Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Code Style

We use:
- Black for code formatting
- isort for import sorting
- flake8 for linting
"""
    (dev_dir / 'contributing.md').write_text(contrib_content)
    
    # testing.md
    testing_content = """# Testing

## Running Tests

```bash
pytest
```

## With Coverage

```bash
pytest --cov=app --cov-report=html
```

## Test Structure

Tests are located in the `tests/` directory.
"""
    (dev_dir / 'testing.md').write_text(testing_content)


def generate_sphinx(project_path: Path, framework: Optional[str] = None) -> Path:
    """
    Generate Sphinx documentation setup.
    
    Args:
        project_path: Path to project root
        framework: Detected framework name
        
    Returns:
        Path to created docs directory
    """
    docs_dir = project_path / 'docs'
    docs_dir.mkdir(exist_ok=True)
    
    # Create conf.py
    conf_content = """# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = '{{ project_name }}'
copyright = '2024, Developer'
author = 'Developer'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Extension configuration -------------------------------------------------

autodoc_mock_imports = []
"""
    
    # Replace placeholder
    try:
        project_name = project_path.name
        conf_content = conf_content.replace('{{ project_name }}', project_name)
    except:
        pass
    
    conf_file = docs_dir / 'conf.py'
    conf_file.write_text(conf_content)
    
    # Create index.rst
    index_content = """{{ project_name }} Documentation
===============================

Welcome to the documentation!

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   api/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""
    
    try:
        project_name = project_path.name
        index_content = index_content.replace('{{ project_name }}', project_name)
    except:
        pass
    
    index_file = docs_dir / 'index.rst'
    index_file.write_text(index_content)
    
    # Create installation.rst
    install_content = """Installation
============

Requirements
-----------

- Python 3.8+
- pip

Install from Source
-------------------

.. code-block:: bash

   git clone <repository-url>
   cd <project-name>
   pip install -r requirements.txt

Virtual Environment
-------------------

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   pip install -r requirements.txt
"""
    (docs_dir / 'installation.rst').write_text(install_content)
    
    # Create API directory
    api_dir = docs_dir / 'api'
    api_dir.mkdir(exist_ok=True)
    
    # api/index.rst
    api_index = """API Reference
==============

.. toctree::
   :maxdepth: 2

   overview
"""
    (api_dir / 'index.rst').write_text(api_index)
    
    # api/overview.rst
    api_overview = """API Overview
============

This API provides endpoints for various operations.

Base URL
--------

.. code-block:: text

   http://localhost:8000/api/v1

Authentication
--------------

Most endpoints require authentication. Include your API key in the header:

.. code-block:: text

   Authorization: Bearer <your-token>
"""
    (api_dir / 'overview.rst').write_text(api_overview)
    
    # Create _static and _templates directories
    (docs_dir / '_static').mkdir(exist_ok=True)
    (docs_dir / '_templates').mkdir(exist_ok=True)
    
    # Create Makefile for Sphinx
    makefile_content = """# Minimal makefile for Sphinx documentation
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help Makefile

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
"""
    (docs_dir / 'Makefile').write_text(makefile_content)
    
    return docs_dir


def update_requirements_for_docs(project_path: Path, tool: str):
    """
    Update requirements-dev.txt with documentation dependencies.
    
    Args:
        project_path: Path to project root
        tool: Documentation tool (mkdocs or sphinx)
    """
    requirements_dev = project_path / 'requirements-dev.txt'
    
    if not requirements_dev.exists():
        requirements_dev = project_path / 'requirements-dev.txt'
        requirements_dev.touch()
    
    try:
        content = requirements_dev.read_text(encoding='utf-8')
        
        if tool == 'mkdocs':
            if 'mkdocs' not in content.lower():
                content += '\nmkdocs>=1.5.0\nmkdocs-material>=9.0.0\n'
        elif tool == 'sphinx':
            if 'sphinx' not in content.lower():
                content += '\nsphinx>=7.0.0\nsphinx-rtd-theme>=1.3.0\n'
        
        requirements_dev.write_text(content, encoding='utf-8')
    except Exception:
        pass

