"""Add command for scaffolding components"""
import click
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from typing import Optional

from ..utils.detector import detect_framework
from ..utils.codegen import (
    generate_model,
    save_model,
    generate_endpoint,
    save_endpoint,
    generate_service,
    save_service,
    generate_middleware,
    save_middleware
)
from ..utils.quality_tools import add_quality_tools
from ..utils.cicd import (
    generate_github_actions,
    generate_gitlab_ci,
    generate_circleci,
    add_ci_badge_to_readme
)
from ..utils.makefile_utils import generate_makefile
from ..utils.docs_utils import (
    generate_mkdocs,
    generate_sphinx,
    update_requirements_for_docs
)
from ..utils.test_utils import generate_enhanced_test_config

console = Console()


@click.group()
def add():
    """Add components to your project (models, endpoints, services, middleware)"""
    pass


@add.command()
@click.argument('name')
@click.option('--fields', help='Fields in format: name:str,email:str,age:int,is_active:bool')
@click.option('--path', '-p', default='.', help='Project path (default: current directory)')
def model(name, fields, path):
    """Add a new model to the project"""
    project_path = Path(path).resolve()
    
    # Detect framework
    framework = detect_framework(project_path)
    if not framework:
        console.print("[bold red]Error:[/bold red] Could not detect framework. Are you in a Projex project?")
        return
    
    # Parse fields
    if not fields:
        fields = Prompt.ask("[cyan]Enter fields[/cyan] (format: name:str,email:str)", default="")
    
    if not fields:
        console.print("[yellow]No fields provided. Creating empty model.[/yellow]")
        field_list = []
    else:
        field_list = [f.strip().split(':') for f in fields.split(',')]
        field_list = [(f[0].strip(), f[1].strip() if len(f) > 1 else 'str') for f in field_list]
    
    # Generate model
    try:
        model_code = generate_model(framework, name, field_list)
        model_path = save_model(framework, project_path, name, model_code)
        
        console.print(f"[bold green]✓[/bold green] Model [cyan]{name}[/cyan] created at: [dim]{model_path}[/dim]")
        console.print("\n[yellow]Next steps:[/yellow]")
        console.print(f"  - Import and use the model in your code")
        if framework in ['fastapi', 'django', 'flask']:
            console.print(f"  - Run migrations to create database table")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


@add.command()
@click.argument('name')
@click.option('--crud', is_flag=True, help='Generate full CRUD endpoints')
@click.option('--path', '-p', default='.', help='Project path (default: current directory)')
def endpoint(name, crud, path):
    """Add a new endpoint/route to the project"""
    project_path = Path(path).resolve()
    
    # Detect framework
    framework = detect_framework(project_path)
    if not framework:
        console.print("[bold red]Error:[/bold red] Could not detect framework. Are you in a Projex project?")
        return
    
    # Generate endpoint
    try:
        endpoint_code = generate_endpoint(framework, name, crud)
        endpoint_path = save_endpoint(framework, project_path, name, endpoint_code, crud)
        
        console.print(f"[bold green]✓[/bold green] Endpoint [cyan]{name}[/cyan] created at: [dim]{endpoint_path}[/dim]")
        console.print("\n[yellow]Next steps:[/yellow]")
        console.print(f"  - Register the endpoint in your router/urls")
        if crud:
            console.print(f"  - Create a model for {name} if you haven't already")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


@add.command()
@click.argument('name')
@click.option('--async', 'is_async', is_flag=True, help='Generate async service')
@click.option('--path', '-p', default='.', help='Project path (default: current directory)')
def service(name, is_async, path):
    """Add a new service class to the project"""
    project_path = Path(path).resolve()
    
    # Detect framework
    framework = detect_framework(project_path)
    if not framework:
        console.print("[bold red]Error:[/bold red] Could not detect framework. Are you in a Projex project?")
        return
    
    # Generate service
    try:
        service_code = generate_service(framework, name, is_async)
        service_path = save_service(framework, project_path, name, service_code)
        
        console.print(f"[bold green]✓[/bold green] Service [cyan]{name}[/cyan] created at: [dim]{service_path}[/dim]")
        console.print("\n[yellow]Next steps:[/yellow]")
        console.print(f"  - Implement your business logic in the service")
        console.print(f"  - Use the service in your endpoints/views")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


@add.command()
@click.argument('name')
@click.option('--path', '-p', default='.', help='Project path (default: current directory)')
def middleware(name, path):
    """Add a new middleware to the project"""
    project_path = Path(path).resolve()
    
    # Detect framework
    framework = detect_framework(project_path)
    if not framework:
        console.print("[bold red]Error:[/bold red] Could not detect framework. Are you in a Projex project?")
        return
    
    # Generate middleware
    try:
        middleware_code = generate_middleware(framework, name)
        middleware_path = save_middleware(framework, project_path, name, middleware_code)
        
        console.print(f"[bold green]✓[/bold green] Middleware [cyan]{name}[/cyan] created at: [dim]{middleware_path}[/dim]")
        console.print("\n[yellow]Next steps:[/yellow]")
        console.print(f"  - Register the middleware in your application")
        console.print(f"  - Configure middleware settings if needed")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


@add.command(name='quality-tools')
@click.option('--path', '-p', default='.', help='Project path (default: current directory)')
def quality_tools(path):
    """Add code quality tools (black, isort, flake8, mypy, pylint) and pre-commit hooks"""
    project_path = Path(path).resolve()
    
    if not (project_path / 'requirements.txt').exists() and not (project_path / 'requirements-dev.txt').exists():
        console.print("[bold red]Error:[/bold red] No requirements files found. Are you in a Python project?")
        return
    
    try:
        add_quality_tools(project_path)
        
        console.print("[bold green]✓[/bold green] Quality tools added successfully!")
        console.print("\n[yellow]Next steps:[/yellow]")
        console.print("  1. Install dependencies: pip install -r requirements-dev.txt")
        console.print("  2. Install pre-commit: pip install pre-commit")
        console.print("  3. Install hooks: pre-commit install")
        console.print("  4. Run manually: pre-commit run --all-files")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


@add.command()
@click.option('--provider', '-p', 
              type=click.Choice(['github', 'gitlab', 'circle']),
              default='github',
              help='CI/CD provider (default: github)')
@click.option('--path', default='.', help='Project path (default: current directory)')
def cicd(provider, path):
    """Add CI/CD pipeline configuration"""
    project_path = Path(path).resolve()
    
    # Detect framework
    framework = detect_framework(project_path)
    
    try:
        if provider == 'github':
            workflow_file = generate_github_actions(project_path, framework)
            console.print(f"[bold green]✓[/bold green] GitHub Actions workflow created at: [dim]{workflow_file}[/dim]")
            add_ci_badge_to_readme(project_path, 'github')
            console.print("[yellow]Note:[/yellow] Update the badge URL in README.md with your GitHub username and repo name")
        
        elif provider == 'gitlab':
            gitlab_file = generate_gitlab_ci(project_path, framework)
            console.print(f"[bold green]✓[/bold green] GitLab CI configuration created at: [dim]{gitlab_file}[/dim]")
            add_ci_badge_to_readme(project_path, 'gitlab')
            console.print("[yellow]Note:[/yellow] Update the badge URL in README.md with your GitLab username and repo name")
        
        elif provider == 'circle':
            circle_file = generate_circleci(project_path, framework)
            console.print(f"[bold green]✓[/bold green] CircleCI configuration created at: [dim]{circle_file}[/dim]")
            add_ci_badge_to_readme(project_path, 'circle')
            console.print("[yellow]Note:[/yellow] Update the badge URL in README.md with your CircleCI username and repo name")
        
        console.print("\n[yellow]Next steps:[/yellow]")
        console.print("  1. Review and customize the CI/CD configuration")
        console.print("  2. Commit and push to trigger the pipeline")
        console.print("  3. Check your CI/CD provider dashboard for build status")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


@add.command()
@click.option('--path', default='.', help='Project path (default: current directory)')
def makefile(path):
    """Generate Makefile with common development tasks"""
    project_path = Path(path).resolve()
    
    # Detect framework
    framework = detect_framework(project_path)
    
    if (project_path / 'Makefile').exists():
        if not Prompt.ask("[yellow]Makefile already exists. Overwrite?[/yellow]", default=False):
            console.print("[yellow]Cancelled.[/yellow]")
            return
    
    try:
        makefile_path = generate_makefile(project_path, framework)
        
        console.print(f"[bold green]✓[/bold green] Makefile created at: [dim]{makefile_path}[/dim]")
        console.print("\n[yellow]Available commands:[/yellow]")
        console.print("  [cyan]make help[/cyan]        - Show all available commands")
        console.print("  [cyan]make install[/cyan]     - Install dependencies")
        console.print("  [cyan]make test[/cyan]        - Run tests")
        console.print("  [cyan]make run[/cyan]         - Run development server")
        console.print("  [cyan]make docker-up[/cyan]    - Start Docker containers")
        console.print("  [cyan]make format[/cyan]       - Format code")
        console.print("\n[yellow]Tip:[/yellow] Run [cyan]make help[/cyan] to see all commands")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


@add.command()
@click.option('--tool', '-t',
              type=click.Choice(['mkdocs', 'sphinx']),
              default='mkdocs',
              help='Documentation tool (default: mkdocs)')
@click.option('--path', default='.', help='Project path (default: current directory)')
def docs(tool, path):
    """Add documentation setup (MkDocs or Sphinx)"""
    project_path = Path(path).resolve()
    
    # Detect framework
    framework = detect_framework(project_path)
    
    try:
        if tool == 'mkdocs':
            mkdocs_file = generate_mkdocs(project_path, framework)
            update_requirements_for_docs(project_path, 'mkdocs')
            
            console.print(f"[bold green]✓[/bold green] MkDocs documentation setup created!")
            console.print(f"\n[yellow]Files created:[/yellow]")
            console.print(f"  - [cyan]mkdocs.yml[/cyan]")
            console.print(f"  - [cyan]docs/[/cyan] directory with initial content")
            
            console.print("\n[yellow]Next steps:[/yellow]")
            console.print("  1. Install dependencies: pip install -r requirements-dev.txt")
            console.print("  2. Start development server: mkdocs serve")
            console.print("  3. Build documentation: mkdocs build")
            console.print("  4. Deploy to GitHub Pages: mkdocs gh-deploy")
        
        elif tool == 'sphinx':
            docs_dir = generate_sphinx(project_path, framework)
            update_requirements_for_docs(project_path, 'sphinx')
            
            console.print(f"[bold green]✓[/bold green] Sphinx documentation setup created!")
            console.print(f"\n[yellow]Files created:[/yellow]")
            console.print(f"  - [cyan]docs/conf.py[/cyan]")
            console.print(f"  - [cyan]docs/index.rst[/cyan]")
            console.print(f"  - [cyan]docs/[/cyan] directory with initial content")
            
            console.print("\n[yellow]Next steps:[/yellow]")
            console.print("  1. Install dependencies: pip install -r requirements-dev.txt")
            console.print("  2. Build documentation: cd docs && make html")
            console.print("  3. View documentation: open _build/html/index.html")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


@add.command(name='test-config')
@click.option('--enhanced', is_flag=True, help='Generate enhanced test configuration')
@click.option('--path', default='.', help='Project path (default: current directory)')
def test_config(enhanced, path):
    """Add enhanced testing configuration (pytest.ini, conftest.py, fixtures)"""
    project_path = Path(path).resolve()
    
    # Detect framework
    framework = detect_framework(project_path)
    
    try:
        pytest_file = generate_enhanced_test_config(project_path, framework)
        
        console.print(f"[bold green]✓[/bold green] Enhanced test configuration created!")
        console.print(f"\n[yellow]Files created:[/yellow]")
        console.print(f"  - [cyan]pytest.ini[/cyan] - Pytest configuration")
        console.print(f"  - [cyan]tests/conftest.py[/cyan] - Shared fixtures")
        console.print(f"  - [cyan]tests/fixtures/factories.py[/cyan] - Test data factories")
        console.print(f"  - [cyan].coveragerc[/cyan] - Coverage configuration")
        
        console.print("\n[yellow]Next steps:[/yellow]")
        console.print("  1. Run tests: pytest")
        console.print("  2. Run with coverage: pytest --cov=app")
        console.print("  3. View HTML coverage: pytest --cov=app --cov-report=html")
        console.print("  4. Run specific markers: pytest -m unit")
        console.print("  5. Skip slow tests: pytest -m 'not slow'")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

