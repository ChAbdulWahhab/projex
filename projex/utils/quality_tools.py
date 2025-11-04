"""Quality tools setup utilities"""
from pathlib import Path
from typing import List


def add_quality_tools(project_path: Path):
    """Add quality tools configuration to project"""
    
    # Create .pre-commit-config.yaml
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
        args: ['--max-line-length=88', '--extend-ignore=E203']

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--ignore-missing-imports]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: debug-statements
'''
    (project_path / '.pre-commit-config.yaml').write_text(pre_commit_config)
    
    # Create or update pyproject.toml
    pyproject_toml_path = project_path / 'pyproject.toml'
    if pyproject_toml_path.exists():
        # Read existing and merge
        existing_content = pyproject_toml_path.read_text()
        new_content = _merge_pyproject_config(existing_content)
        pyproject_toml_path.write_text(new_content)
    else:
        # Create new
        pyproject_content = '''[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']
include = '\\.pyi?$'
extend-exclude = \"\"\"
  /(
      # directories
      \\.eggs
    | \\.git
    | \\.hg
    | \\.mypy_cache
    | \\.tox
    | \\.venv
    | venv
    | _build
    | buck-out
    | build
    | dist
  )/
\"\"\"

[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
skip_glob = ["*/migrations/*", "*/venv/*", "*/__pycache__/*"]

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "E266", "E501", "W503"]
exclude = [
    ".git",
    "__pycache__",
    "build",
    "dist",
    ".venv",
    "venv",
    "migrations",
]

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
ignore_missing_imports = true
exclude = [
    "migrations/",
    "venv/",
    ".venv/",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
source = ["app"]
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/migrations/*",
    "*/venv/*",
    "*/.venv/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@abstractmethod",
]

[tool.pylint.messages_control]
disable = [
    "C0111",  # missing-docstring
    "C0103",  # invalid-name
    "R0903",  # too-few-public-methods
    "R0913",  # too-many-arguments
]
'''
        pyproject_toml_path.write_text(pyproject_content)
    
    # Update requirements-dev.txt
    dev_requirements_path = project_path / 'requirements-dev.txt'
    quality_packages = [
        'pre-commit>=3.5.0',
        'black>=23.12.0',
        'isort>=5.13.2',
        'flake8>=7.0.0',
        'mypy>=1.7.0',
        'pylint>=3.0.0',
        'pytest-cov>=4.1.0',
    ]
    
    if dev_requirements_path.exists():
        content = dev_requirements_path.read_text()
        # Add quality packages if not present
        for package in quality_packages:
            if package.split('>=')[0] not in content:
                content += f'\n{package}'
        dev_requirements_path.write_text(content)
    else:
        # Create requirements-dev.txt
        base_requirements = '-r requirements.txt\n' if (project_path / 'requirements.txt').exists() else ''
        dev_requirements_path.write_text(base_requirements + '\n'.join(quality_packages))
    
    # Create GitHub Actions workflow
    workflows_dir = project_path / '.github' / 'workflows'
    workflows_dir.mkdir(parents=True, exist_ok=True)
    
    ci_workflow = '''name: CI

on:
  push:
    branches: [ main, develop, master ]
  pull_request:
    branches: [ main, develop, master ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
    
    - name: Run black
      run: black --check .
    
    - name: Run isort
      run: isort --check-only .
    
    - name: Run flake8
      run: flake8 .
    
    - name: Run mypy
      run: mypy . || true  # Allow mypy to fail for now
    
    - name: Run pylint
      run: pylint app/ || true  # Allow pylint to fail for now

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
      run: pytest
    
    - name: Generate coverage report
      run: pytest --cov=app --cov-report=xml --cov-report=html
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: false
'''
    (workflows_dir / 'ci.yml').write_text(ci_workflow)
    
    # Update README with quality tools section
    readme_path = project_path / 'README.md'
    if readme_path.exists():
        content = readme_path.read_text()
        if '## Code Quality' not in content:
            quality_section = '''
## Code Quality

This project uses several tools to maintain code quality:

- **black** - Code formatting
- **isort** - Import sorting
- **flake8** - Linting
- **mypy** - Type checking
- **pylint** - Advanced linting
- **pytest** - Testing

### Pre-commit Hooks

Install pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

Run hooks manually:

```bash
pre-commit run --all-files
```

### Running Quality Checks

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .
pylint app/

# Type check
mypy .
```
'''
            # Insert before "## Author" section
            if '## Author' in content:
                content = content.replace('## Author', quality_section + '\n\n## Author')
            else:
                content += quality_section
            readme_path.write_text(content)


def _merge_pyproject_config(existing_content: str) -> str:
    """Merge new tool configurations with existing pyproject.toml"""
    # Simple merge - append new sections if they don't exist
    new_sections = {
        '[tool.black]': '''[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']
''',
        '[tool.isort]': '''[tool.isort]
profile = "black"
line_length = 88
''',
        '[tool.pytest.ini_options]': '''[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --tb=short"
''',
    }
    
    # Check if sections exist
    for section, config in new_sections.items():
        if section not in existing_content:
            existing_content += '\n\n' + config
    
    return existing_content

