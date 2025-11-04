"""Validation and info commands"""
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import subprocess
import sys
import os
from datetime import datetime
from typing import Optional, Dict, List

from ..utils.detector import detect_framework

console = Console()


def _check_file_exists(project_path: Path, filename: str) -> bool:
    """Check if a file exists"""
    return (project_path / filename).exists()


def _check_directory_exists(project_path: Path, dirname: str) -> bool:
    """Check if a directory exists"""
    return (project_path / dirname).exists() and (project_path / dirname).is_dir()


def _count_lines_of_code(project_path: Path) -> int:
    """Count total lines of code in Python files"""
    total_lines = 0
    for py_file in project_path.rglob('*.py'):
        # Skip virtual environments and cache
        if 'venv' in str(py_file) or '__pycache__' in str(py_file) or '.venv' in str(py_file):
            continue
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                total_lines += len([line for line in f if line.strip()])
        except:
            pass
    return total_lines


def _count_files(project_path: Path) -> int:
    """Count total Python files"""
    count = 0
    for py_file in project_path.rglob('*.py'):
        if 'venv' not in str(py_file) and '__pycache__' not in str(py_file) and '.venv' not in str(py_file):
            count += 1
    return count


def _parse_requirements(requirements_path: Path) -> Dict[str, List[str]]:
    """Parse requirements.txt and return dependencies"""
    if not requirements_path.exists():
        return {'dependencies': [], 'dev_dependencies': []}
    
    deps = []
    dev_deps = []
    is_dev = False
    
    try:
        with open(requirements_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line == '-r requirements.txt':
                    is_dev = True
                    continue
                if is_dev:
                    dev_deps.append(line.split('>=')[0].split('==')[0])
                else:
                    deps.append(line.split('>=')[0].split('==')[0])
    except:
        pass
    
    return {'dependencies': deps, 'dev_dependencies': dev_deps}


def _get_git_status(project_path: Path) -> str:
    """Get git status"""
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            if result.stdout.strip():
                return "Has uncommitted changes"
            else:
                return "Clean"
    except:
        pass
    return "Not a git repository"


def _get_last_modified(project_path: Path) -> str:
    """Get last modified time of project"""
    try:
        # Get most recent file modification
        most_recent = 0
        for file_path in project_path.rglob('*'):
            if file_path.is_file() and 'venv' not in str(file_path):
                try:
                    mtime = file_path.stat().st_mtime
                    if mtime > most_recent:
                        most_recent = mtime
                except:
                    pass
        
        if most_recent:
            mod_time = datetime.fromtimestamp(most_recent)
            days_ago = (datetime.now() - mod_time).days
            if days_ago == 0:
                return "Today"
            elif days_ago == 1:
                return "1 day ago"
            else:
                return f"{days_ago} days ago"
    except:
        pass
    return "Unknown"


def _count_tests(project_path: Path) -> int:
    """Count test files"""
    test_count = 0
    for test_file in project_path.rglob('test_*.py'):
        if 'venv' not in str(test_file) and '__pycache__' not in str(test_file) and '.venv' not in str(test_file):
            test_count += 1
    # Also check for tests.py in Django
    for tests_file in project_path.rglob('tests.py'):
        if 'venv' not in str(tests_file) and '__pycache__' not in str(tests_file) and '.venv' not in str(tests_file):
            test_count += 1
    return test_count


def _check_docker(project_path: Path) -> bool:
    """Check if Docker is configured"""
    return _check_file_exists(project_path, 'Dockerfile') and _check_file_exists(project_path, 'docker-compose.yml')


def _get_python_version() -> str:
    """Get Python version"""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def _get_framework_version(framework: Optional[str], project_path: Path) -> str:
    """Try to get framework version from requirements"""
    requirements_path = project_path / 'requirements.txt'
    if not requirements_path.exists():
        return "Unknown"
    
    try:
        with open(requirements_path, 'r') as f:
            content = f.read()
            if framework == 'fastapi':
                if 'fastapi>=' in content:
                    import re
                    match = re.search(r'fastapi>=([\d.]+)', content)
                    if match:
                        return match.group(1)
            elif framework == 'django':
                if 'Django>=' in content:
                    import re
                    match = re.search(r'Django>=([\d.]+)', content)
                    if match:
                        return match.group(1)
            elif framework == 'flask':
                if 'Flask>=' in content:
                    import re
                    match = re.search(r'Flask>=([\d.]+)', content)
                    if match:
                        return match.group(1)
    except:
        pass
    
    return "Unknown"


@click.command()
@click.option('--path', '-p', default='.', help='Project path (default: current directory)')
def validate(path):
    """Validate project structure and configuration"""
    project_path = Path(path).resolve()
    
    console.print("\n[bold cyan]Validating project structure...[/bold cyan]\n")
    
    errors = []
    warnings = []
    
    # Check required files
    required_files = ['requirements.txt', '.gitignore', 'README.md']
    for filename in required_files:
        if not _check_file_exists(project_path, filename):
            errors.append(f"Missing required file: {filename}")
    
    # Check project structure
    framework = detect_framework(project_path)
    if framework:
        if framework == 'fastapi':
            if not _check_directory_exists(project_path, 'app'):
                errors.append("Missing 'app' directory")
            if not _check_file_exists(project_path, 'app/main.py'):
                errors.append("Missing 'app/main.py'")
        
        elif framework == 'django':
            if not _check_file_exists(project_path, 'manage.py'):
                errors.append("Missing 'manage.py'")
            if not _check_directory_exists(project_path, 'config'):
                errors.append("Missing 'config' directory")
        
        elif framework == 'flask':
            if not _check_directory_exists(project_path, 'app'):
                errors.append("Missing 'app' directory")
            if not _check_file_exists(project_path, 'run.py'):
                warnings.append("Missing 'run.py' (optional)")
    else:
        warnings.append("Could not detect framework (may not be a Projex project)")
    
    # Check requirements.txt validity
    if _check_file_exists(project_path, 'requirements.txt'):
        try:
            with open(project_path / 'requirements.txt', 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines, 1):
                    line = line.strip()
                    if line and not line.startswith('#') and '==' not in line and '>=' not in line and '~=' not in line:
                        if not line.startswith('-r'):
                            warnings.append(f"requirements.txt line {i} may have invalid format: {line}")
        except Exception as e:
            errors.append(f"Error reading requirements.txt: {str(e)}")
    
    # Check .env.example
    if _check_file_exists(project_path, '.env.example'):
        if not _check_file_exists(project_path, '.env'):
            warnings.append(".env file not found (copy from .env.example)")
    
    # Check Docker
    has_docker = _check_docker(project_path)
    if not has_docker:
        warnings.append("Docker configuration not found (optional)")
    
    # Check tests
    test_count = _count_tests(project_path)
    if test_count == 0:
        warnings.append("No test files found")
    
    # Display results
    if errors:
        console.print("[bold red]Errors:[/bold red]")
        for error in errors:
            console.print(f"  [red]✗[/red] {error}")
        console.print()
    
    if warnings:
        console.print("[bold yellow]Warnings:[/bold yellow]")
        for warning in warnings:
            console.print(f"  [yellow]⚠[/yellow] {warning}")
        console.print()
    
    if not errors and not warnings:
        console.print("[bold green]✓[/bold green] Project structure is valid!")
        return
    
    if errors:
        console.print("[bold red]Validation failed![/bold red]")
        sys.exit(1)
    else:
        console.print("[bold yellow]Validation passed with warnings.[/bold yellow]")


@click.command()
@click.option('--path', '-p', default='.', help='Project path (default: current directory)')
def info(path):
    """Display project information"""
    project_path = Path(path).resolve()
    
    console.print("\n[bold cyan]Project Information[/bold cyan]\n")
    
    # Get project name
    project_name = project_path.name
    
    # Detect framework
    framework = detect_framework(project_path)
    framework_name = framework.capitalize() if framework else "Unknown"
    framework_version = _get_framework_version(framework, project_path) if framework else "N/A"
    
    # Get stats
    total_files = _count_files(project_path)
    lines_of_code = _count_lines_of_code(project_path)
    
    # Get dependencies
    requirements_path = project_path / 'requirements.txt'
    deps_info = _parse_requirements(requirements_path)
    total_deps = len(deps_info['dependencies'])
    total_dev_deps = len(deps_info['dev_dependencies'])
    
    # Get other info
    git_status = _get_git_status(project_path)
    last_modified = _get_last_modified(project_path)
    docker_configured = "✓" if _check_docker(project_path) else "✗"
    test_count = _count_tests(project_path)
    
    # Create info table
    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
    table.add_row("[cyan]Project:[/cyan]", project_name)
    table.add_row("[cyan]Template:[/cyan]", framework_name)
    if framework:
        table.add_row("[cyan]Framework Version:[/cyan]", framework_version)
    table.add_row("[cyan]Python Version:[/cyan]", _get_python_version())
    table.add_row("[cyan]Total Files:[/cyan]", str(total_files))
    table.add_row("[cyan]Lines of Code:[/cyan]", f"{lines_of_code:,}")
    table.add_row("[cyan]Total Dependencies:[/cyan]", str(total_deps))
    table.add_row("[cyan]Dev Dependencies:[/cyan]", str(total_dev_deps))
    table.add_row("[cyan]Last Modified:[/cyan]", last_modified)
    table.add_row("[cyan]Git Status:[/cyan]", git_status)
    table.add_row("[cyan]Docker:[/cyan]", docker_configured)
    table.add_row("[cyan]Tests:[/cyan]", f"{test_count} test files found")
    
    # Try to get coverage if available
    coverage_file = project_path / '.coverage'
    if coverage_file.exists():
        table.add_row("[cyan]Coverage:[/cyan]", "Available (run pytest --cov to update)")
    else:
        table.add_row("[cyan]Coverage:[/cyan]", "Not available")
    
    console.print(table)
    console.print()


@click.command()
@click.option('--path', '-p', default='.', help='Project path (default: current directory)')
def doctor(path):
    """Alias for validate command - check project health"""
    validate.callback(path)


# Register commands
def register_commands(main_group):
    """Register validation and info commands"""
    main_group.add_command(validate)
    main_group.add_command(info)
    main_group.add_command(doctor)

