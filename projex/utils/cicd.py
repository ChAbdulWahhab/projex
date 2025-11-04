"""CI/CD pipeline generation utilities"""
from pathlib import Path
from typing import Optional
from jinja2 import Template


def generate_github_actions(project_path: Path, framework: Optional[str] = None) -> Path:
    """
    Generate GitHub Actions CI/CD workflow.
    
    Args:
        project_path: Path to project root
        framework: Detected framework name
        
    Returns:
        Path to created workflow file
    """
    workflows_dir = project_path / '.github' / 'workflows'
    workflows_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine Python version and test command based on framework
    python_version = '3.11'
    test_command = 'pytest'
    run_command = ''
    
    if framework == 'django':
        test_command = 'python manage.py test'
        run_command = 'python manage.py runserver'
    elif framework == 'fastapi':
        run_command = 'uvicorn app.main:app --host 0.0.0.0 --port 8000'
    elif framework == 'flask':
        run_command = 'python run.py'
    elif framework in ['bottle', 'tornado', 'sanic', 'cherrypy', 'pyramid']:
        run_command = 'python app/main.py'
    
    workflow_content = f"""name: CI

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{{{ matrix.python-version }}}}
      uses: actions/setup-python@v5
      with:
        python-version: ${{{{ matrix.python-version }}}}
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run linting
      run: |
        black --check .
        isort --check-only .
        flake8 . || true
      continue-on-error: true
    
    - name: Run tests
      run: {test_command}
    
    - name: Check code coverage
      run: |
        pytest --cov=app --cov-report=xml --cov-report=term-missing || true
      continue-on-error: true
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: false
      continue-on-error: true

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '{python_version}'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Build Docker image
      run: |
        docker build -t ${{{{ github.repository }}}}:${{{{ github.sha }}}} .
      continue-on-error: true
    
    # Uncomment for deployment
    # - name: Deploy to production
    #   if: github.ref == 'refs/heads/main'
    #   run: |
    #     echo "Add your deployment commands here"
"""
    
    workflow_file = workflows_dir / 'ci.yml'
    workflow_file.write_text(workflow_content)
    
    return workflow_file


def generate_gitlab_ci(project_path: Path, framework: Optional[str] = None) -> Path:
    """
    Generate GitLab CI/CD configuration.
    
    Args:
        project_path: Path to project root
        framework: Detected framework name
        
    Returns:
        Path to created .gitlab-ci.yml file
    """
    # Determine test command based on framework
    test_command = 'pytest'
    
    if framework == 'django':
        test_command = 'python manage.py test'
    
    gitlab_ci_content = f"""stages:
  - test
  - lint
  - build
  # - deploy

variables:
  PYTHON_VERSION: "3.11"
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip

before_script:
  - python --version
  - pip install --upgrade pip
  - pip install -r requirements.txt
  - pip install -r requirements-dev.txt

test:
  stage: test
  image: python:${{PYTHON_VERSION}}
  script:
    - {test_command}
  coverage: '/TOTAL.*\\s+(\\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
    paths:
      - coverage.xml
    expire_in: 1 week

lint:
  stage: lint
  image: python:${{PYTHON_VERSION}}
  script:
    - black --check . || true
    - isort --check-only . || true
    - flake8 . || true
    - mypy . || true
  allow_failure: true

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - apk add --no-cache docker-cli
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE:latest
  only:
    - main
    - master
  # Uncomment to push to registry
  # - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  # - docker push $CI_REGISTRY_IMAGE:latest

# Uncomment for deployment
# deploy:
#   stage: deploy
#   image: alpine:latest
#   script:
#     - echo "Add your deployment commands here"
#   only:
#     - main
#     - master
"""
    
    gitlab_ci_file = project_path / '.gitlab-ci.yml'
    gitlab_ci_file.write_text(gitlab_ci_content)
    
    return gitlab_ci_file


def generate_circleci(project_path: Path, framework: Optional[str] = None) -> Path:
    """
    Generate CircleCI configuration.
    
    Args:
        project_path: Path to project root
        framework: Detected framework name
        
    Returns:
        Path to created .circleci/config.yml file
    """
    circleci_dir = project_path / '.circleci'
    circleci_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine test command based on framework
    test_command = 'pytest'
    
    if framework == 'django':
        test_command = 'python manage.py test'
    
    circleci_content = f"""version: 2.1

orbs:
  python: circleci/python@2.1.1

workflows:
  test_and_build:
    jobs:
      - test
      - build:
          requires:
            - test

jobs:
  test:
    docker:
      - image: cimg/python:3.11
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: pip
          pip-dependency-file: requirements.txt
      - run:
          name: Install dev dependencies
          command: pip install -r requirements-dev.txt
      - run:
          name: Run linting
          command: |
            black --check . || true
            isort --check-only . || true
            flake8 . || true
      - run:
          name: Run tests
          command: {test_command}
      - run:
          name: Generate coverage report
          command: |
            pytest --cov=app --cov-report=xml --cov-report=term-missing || true
      - store_artifacts:
          path: coverage.xml
          destination: coverage

  build:
    docker:
      - image: cimg/python:3.11
    steps:
      - checkout
      - setup_remote_docker:
          docker_layer_caching: true
      - run:
          name: Build Docker image
          command: |
            docker build -t ${{CIRCLE_PROJECT_REPONAME}}:${{CIRCLE_SHA1}} .
      # Uncomment for deployment
      # - run:
      #     name: Deploy
      #     command: |
      #       echo "Add your deployment commands here"
"""
    
    config_file = circleci_dir / 'config.yml'
    config_file.write_text(circleci_content)
    
    return config_file


def add_ci_badge_to_readme(project_path: Path, provider: str) -> bool:
    """
    Add CI badge to README.md.
    
    Args:
        project_path: Path to project root
        provider: CI provider (github, gitlab, circle)
        
    Returns:
        True if badge was added, False otherwise
    """
    readme_path = project_path / 'README.md'
    
    if not readme_path.exists():
        return False
    
    try:
        readme_content = readme_path.read_text(encoding='utf-8')
        
        # Check if badge already exists
        if '![CI' in readme_content or f'{provider}' in readme_content.lower():
            return False
        
        # Generate badge based on provider
        if provider == 'github':
            badge = '[![CI](https://github.com/USERNAME/REPO/workflows/CI/badge.svg)](https://github.com/USERNAME/REPO/actions)'
        elif provider == 'gitlab':
            badge = '[![pipeline status](https://gitlab.com/USERNAME/REPO/badges/main/pipeline.svg)](https://gitlab.com/USERNAME/REPO/-/commits/main)'
        elif provider == 'circle':
            badge = '[![CircleCI](https://circleci.com/gh/USERNAME/REPO.svg?style=svg)](https://circleci.com/gh/USERNAME/REPO)'
        else:
            return False
        
        # Add badge after first heading
        lines = readme_content.split('\n')
        insert_index = 0
        
        for i, line in enumerate(lines):
            if line.startswith('# '):
                insert_index = i + 1
                break
        
        lines.insert(insert_index, f'\n{badge}\n')
        readme_path.write_text('\n'.join(lines), encoding='utf-8')
        
        return True
    except Exception:
        return False

