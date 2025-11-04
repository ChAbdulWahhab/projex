"""Dependency management utilities"""
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def check_outdated_packages(project_path: Path) -> List[Dict[str, str]]:
    """
    Check for outdated packages using pip list --outdated.
    
    Args:
        project_path: Path to project root
        
    Returns:
        List of outdated packages with current and latest versions
    """
    outdated = []
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'list', '--outdated', '--format=json'],
            capture_output=True,
            text=True,
            cwd=project_path,
            timeout=30
        )
        
        if result.returncode == 0:
            import json
            packages = json.loads(result.stdout)
            for pkg in packages:
                outdated.append({
                    'name': pkg.get('name', ''),
                    'current': pkg.get('version', ''),
                    'latest': pkg.get('latest_version', '')
                })
    except Exception as e:
        console.print(f"[yellow]Warning:[/yellow] Could not check outdated packages: {str(e)}")
    
    return outdated


def audit_packages(project_path: Path) -> List[Dict[str, str]]:
    """
    Security audit packages using pip-audit.
    
    Args:
        project_path: Path to project root
        
    Returns:
        List of vulnerable packages
    """
    vulnerabilities = []
    
    try:
        # Check if pip-audit is installed
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', 'pip-audit'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            console.print("[yellow]pip-audit not installed. Installing...[/yellow]")
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', 'pip-audit'],
                capture_output=True,
                text=True
            )
        
        # Run pip-audit
        result = subprocess.run(
            [sys.executable, '-m', 'pip_audit', '--format=json'],
            capture_output=True,
            text=True,
            cwd=project_path,
            timeout=60
        )
        
        if result.returncode == 0:
            import json
            try:
                audit_data = json.loads(result.stdout)
                for vuln in audit_data.get('vulnerabilities', []):
                    vulnerabilities.append({
                        'package': vuln.get('name', ''),
                        'installed': vuln.get('installed_version', ''),
                        'vulnerability': vuln.get('vulnerability', {}).get('id', ''),
                        'severity': vuln.get('vulnerability', {}).get('severity', 'UNKNOWN'),
                        'description': vuln.get('vulnerability', {}).get('description', '')
                    })
            except json.JSONDecodeError:
                # pip-audit might output text format
                pass
        elif result.stderr:
            # Parse text output if JSON fails
            lines = result.stderr.split('\n')
            for line in lines:
                if 'VULN' in line or 'Found' in line:
                    # Simple parsing
                    pass
    except subprocess.TimeoutExpired:
        console.print("[yellow]Security audit timed out. This may take a while.[/yellow]")
    except FileNotFoundError:
        console.print("[yellow]pip-audit not available. Install it with: pip install pip-audit[/yellow]")
    except Exception as e:
        console.print(f"[yellow]Warning:[/yellow] Could not run security audit: {str(e)}")
    
    return vulnerabilities


def get_requirements_file(project_path: Path) -> Optional[Path]:
    """Find requirements.txt file"""
    requirements = project_path / 'requirements.txt'
    if requirements.exists():
        return requirements
    return None


def parse_requirements(requirements_file: Path) -> List[Dict[str, str]]:
    """
    Parse requirements.txt file.
    
    Args:
        requirements_file: Path to requirements.txt
        
    Returns:
        List of packages with versions
    """
    packages = []
    
    if not requirements_file.exists():
        return packages
    
    try:
        content = requirements_file.read_text(encoding='utf-8')
        for line in content.split('\n'):
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Remove comments from end of line
            if '#' in line:
                line = line.split('#')[0].strip()
            
            # Parse package==version or package>=version etc
            if '==' in line:
                name, version = line.split('==', 1)
                packages.append({'name': name.strip(), 'version': version.strip(), 'spec': '=='})
            elif '>=' in line:
                name, version = line.split('>=', 1)
                packages.append({'name': name.strip(), 'version': version.strip(), 'spec': '>='})
            elif '>' in line:
                name, version = line.split('>', 1)
                packages.append({'name': name.strip(), 'version': version.strip(), 'spec': '>'})
            elif '<=' in line:
                name, version = line.split('<=', 1)
                packages.append({'name': name.strip(), 'version': version.strip(), 'spec': '<='})
            elif '<' in line:
                name, version = line.split('<', 1)
                packages.append({'name': name.strip(), 'version': version.strip(), 'spec': '<'})
            elif '~=' in line:
                name, version = line.split('~=', 1)
                packages.append({'name': name.strip(), 'version': version.strip(), 'spec': '~='})
            else:
                # No version specified
                packages.append({'name': line, 'version': None, 'spec': None})
    except Exception as e:
        console.print(f"[yellow]Warning:[/yellow] Could not parse requirements.txt: {str(e)}")
    
    return packages


def update_package_safely(package_name: str, project_path: Path, interactive: bool = True) -> bool:
    """
    Update a single package safely.
    
    Args:
        package_name: Name of package to update
        project_path: Path to project root
        interactive: Whether to ask for confirmation
        
    Returns:
        True if updated successfully
    """
    try:
        # Check current version
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', package_name],
            capture_output=True,
            text=True,
            cwd=project_path
        )
        
        if result.returncode != 0:
            console.print(f"[red]Package {package_name} not found.[/red]")
            return False
        
        # Update package
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', package_name],
            capture_output=True,
            text=True,
            cwd=project_path
        )
        
        if result.returncode == 0:
            # Update requirements.txt
            requirements_file = get_requirements_file(project_path)
            if requirements_file:
                update_requirements_file(requirements_file, package_name)
            return True
        else:
            console.print(f"[red]Failed to update {package_name}: {result.stderr}[/red]")
            return False
    except Exception as e:
        console.print(f"[red]Error updating {package_name}: {str(e)}[/red]")
        return False


def update_requirements_file(requirements_file: Path, package_name: str):
    """
    Update requirements.txt with latest version of package.
    
    Args:
        requirements_file: Path to requirements.txt
        package_name: Package name
    """
    try:
        # Get installed version
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', package_name],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return
        
        # Extract version
        version = None
        for line in result.stdout.split('\n'):
            if line.startswith('Version:'):
                version = line.split(':', 1)[1].strip()
                break
        
        if not version:
            return
        
        # Update requirements.txt
        content = requirements_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if line.strip().startswith(package_name):
                # Update this line
                if '==' in line:
                    lines[i] = f"{package_name}=={version}"
                elif '>=' in line or '>' in line or '<=' in line or '<' in line or '~=' in line:
                    lines[i] = f"{package_name}=={version}"
                else:
                    lines[i] = f"{package_name}=={version}"
                break
        
        requirements_file.write_text('\n'.join(lines), encoding='utf-8')
    except Exception as e:
        console.print(f"[yellow]Warning:[/yellow] Could not update requirements.txt: {str(e)}")

