"""Environment configuration commands"""
import click
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from typing import Optional

from ..utils.detector import detect_framework
from ..utils.env_utils import (
    generate_env_file,
    list_env_files,
    get_env_variables
)

console = Console()


@click.group()
def env():
    """Manage environment configuration files (.env.development, .env.staging, etc.)"""
    pass


@env.command()
@click.argument('env_name')
@click.option('--path', '-p', default='.', help='Project path (default: current directory)')
@click.option('--db', type=click.Choice(['postgresql', 'mysql', 'mongodb', 'sqlite', 'redis']),
              help='Database type (auto-detected from project if not specified)')
def add(env_name, path, db):
    """Add a new environment configuration file"""
    project_path = Path(path).resolve()
    
    # Validate environment name
    valid_envs = ['development', 'staging', 'production', 'test']
    if env_name.lower() not in valid_envs:
        console.print(f"[bold red]Error:[/bold red] Invalid environment name. Must be one of: {', '.join(valid_envs)}")
        return
    
    env_name = env_name.lower()
    
    # Detect framework and database
    framework = detect_framework(project_path)
    
    # Try to detect database from existing .env.example or docker-compose.yml
    if not db:
        db = _detect_database(project_path)
    
    if not db:
        db = Prompt.ask(
            "[cyan]Database type[/cyan]",
            choices=['postgresql', 'mysql', 'mongodb', 'sqlite', 'redis'],
            default='postgresql'
        )
    
    # Check if file already exists
    if env_name == 'development':
        env_file_path = project_path / '.env.development'
    else:
        env_file_path = project_path / f'.env.{env_name}'
    
    if env_file_path.exists():
        if not Confirm.ask(f"[yellow]File {env_file_path.name} already exists. Overwrite?[/yellow]", default=False):
            console.print("[yellow]Cancelled.[/yellow]")
            return
    
    try:
        env_file = generate_env_file(project_path, env_name, framework, db)
        
        console.print(f"[bold green]✓[/bold green] Environment file created: [cyan]{env_file.name}[/cyan]")
        console.print(f"\n[yellow]Location:[/yellow] [dim]{env_file}[/dim]")
        console.print("\n[yellow]Next steps:[/yellow]")
        console.print("  1. Review and customize the environment variables")
        console.print("  2. Add any project-specific variables")
        console.print("  3. Make sure .env files are in .gitignore (they should be)")
        console.print("  4. Update your application to load the correct .env file")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


@env.command()
@click.option('--path', '-p', default='.', help='Project path (default: current directory)')
def list(path):
    """List all environment configuration files"""
    project_path = Path(path).resolve()
    
    env_files = list_env_files(project_path)
    
    if not env_files:
        console.print("[yellow]No environment files found.[/yellow]")
        console.print("\n[yellow]Tip:[/yellow] Create environment files using:")
        console.print("  [cyan]projex env add development[/cyan]")
        console.print("  [cyan]projex env add staging[/cyan]")
        console.print("  [cyan]projex env add production[/cyan]")
        return
    
    table = Table(title="Environment Files", show_header=True, header_style="bold cyan")
    table.add_column("File", style="cyan", no_wrap=True)
    table.add_column("Size", style="green")
    table.add_column("Variables", style="yellow")
    table.add_column("Modified", style="dim")
    
    for env_file in env_files:
        try:
            size = env_file.stat().st_size
            size_str = f"{size} bytes"
            
            env_vars = get_env_variables(env_file)
            var_count = len(env_vars)
            
            mtime = env_file.stat().st_mtime
            from datetime import datetime
            modified = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
            
            table.add_row(
                env_file.name,
                size_str,
                str(var_count),
                modified
            )
        except Exception:
            table.add_row(env_file.name, "N/A", "N/A", "N/A")
    
    console.print("\n")
    console.print(table)
    console.print(f"\n[dim]Total: {len(env_files)} environment file(s)[/dim]")


@env.command()
@click.argument('env_file_name')
@click.option('--path', '-p', default='.', help='Project path (default: current directory)')
def show(env_file_name, path):
    """Show contents of an environment file"""
    project_path = Path(path).resolve()
    
    # Try to find the file
    env_file = None
    
    # If full name provided
    if env_file_name.startswith('.env'):
        env_file = project_path / env_file_name
    else:
        # Try common patterns
        patterns = [
            f'.env.{env_file_name}',
            f'.env.{env_file_name.lower()}',
            f'.env.{env_file_name.upper()}'
        ]
        
        for pattern in patterns:
            potential_file = project_path / pattern
            if potential_file.exists():
                env_file = potential_file
                break
    
    if not env_file or not env_file.exists():
        console.print(f"[bold red]Error:[/bold red] Environment file not found: {env_file_name}")
        console.print("\n[yellow]Available files:[/yellow]")
        env_files = list_env_files(project_path)
        for f in env_files:
            console.print(f"  - {f.name}")
        return
    
    try:
        env_vars = get_env_variables(env_file)
        
        if not env_vars:
            console.print(f"[yellow]No environment variables found in {env_file.name}[/yellow]")
            return
        
        table = Table(title=f"Environment Variables: {env_file.name}", show_header=True, header_style="bold cyan")
        table.add_column("Variable", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")
        
        for key, value in sorted(env_vars.items()):
            # Mask sensitive values
            if any(sensitive in key.lower() for sensitive in ['secret', 'password', 'key', 'token', 'api_key']):
                value = '*' * min(len(value), 20) + ' (hidden)'
            
            table.add_row(key, value)
        
        console.print("\n")
        console.print(table)
        console.print(f"\n[dim]Total: {len(env_vars)} variable(s)[/dim]")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


def _detect_database(project_path: Path) -> Optional[str]:
    """Try to detect database type from project files"""
    # Check docker-compose.yml
    docker_compose = project_path / 'docker-compose.yml'
    if docker_compose.exists():
        try:
            content = docker_compose.read_text()
            if 'postgres' in content.lower():
                return 'postgresql'
            elif 'mysql' in content.lower():
                return 'mysql'
            elif 'mongo' in content.lower():
                return 'mongodb'
            elif 'redis' in content.lower():
                return 'redis'
        except:
            pass
    
    # Check .env.example
    env_example = project_path / '.env.example'
    if env_example.exists():
        try:
            content = env_example.read_text()
            if 'postgresql://' in content or 'postgres://' in content:
                return 'postgresql'
            elif 'mysql://' in content:
                return 'mysql'
            elif 'mongodb://' in content:
                return 'mongodb'
            elif 'sqlite://' in content:
                return 'sqlite'
            elif 'redis://' in content:
                return 'redis'
        except:
            pass
    
    # Check requirements.txt for database drivers
    requirements = project_path / 'requirements.txt'
    if requirements.exists():
        try:
            content = requirements.read_text().lower()
            if 'psycopg2' in content or 'asyncpg' in content:
                return 'postgresql'
            elif 'pymysql' in content or 'mysqlclient' in content:
                return 'mysql'
            elif 'motor' in content or 'pymongo' in content:
                return 'mongodb'
            elif 'redis' in content:
                return 'redis'
        except:
            pass
    
    return None

