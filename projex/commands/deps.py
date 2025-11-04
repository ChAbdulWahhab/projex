"""Dependency management commands"""
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Confirm

from ..utils.deps_utils import (
    check_outdated_packages,
    audit_packages,
    get_requirements_file,
    parse_requirements,
    update_package_safely
)

console = Console()


@click.group()
def deps():
    """Manage project dependencies (check outdated, update, security audit)"""
    pass


@deps.command()
@click.option('--path', '-p', default='.', help='Project path (default: current directory)')
def check(path):
    """Check for outdated packages"""
    project_path = Path(path).resolve()
    
    requirements_file = get_requirements_file(project_path)
    
    if not requirements_file:
        console.print("[bold red]Error:[/bold red] requirements.txt not found. Are you in a Python project?")
        return
    
    console.print("[cyan]Checking for outdated packages...[/cyan]\n")
    
    try:
        outdated = check_outdated_packages(project_path)
        
        if not outdated:
            console.print("[bold green]✓[/bold green] All packages are up to date!")
            return
        
        table = Table(title="Outdated Packages", show_header=True, header_style="bold cyan")
        table.add_column("Package", style="cyan", no_wrap=True)
        table.add_column("Current Version", style="yellow")
        table.add_column("Latest Version", style="green")
        
        for pkg in outdated:
            table.add_row(
                pkg['name'],
                pkg['current'],
                pkg['latest']
            )
        
        console.print(table)
        console.print(f"\n[dim]Found {len(outdated)} outdated package(s)[/dim]")
        console.print("\n[yellow]Tip:[/yellow] Use [cyan]projex deps update[/cyan] to update packages safely")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


@deps.command()
@click.option('--path', '-p', default='.', help='Project path (default: current directory)')
@click.option('--interactive/--no-interactive', default=True, help='Ask for confirmation before updating each package')
@click.option('--package', help='Update specific package only')
def update(path, interactive, package):
    """Update packages safely (with confirmation)"""
    project_path = Path(path).resolve()
    
    requirements_file = get_requirements_file(project_path)
    
    if not requirements_file:
        console.print("[bold red]Error:[/bold red] requirements.txt not found. Are you in a Python project?")
        return
    
    if package:
        # Update single package
        if interactive:
            if not Confirm.ask(f"[yellow]Update {package}?[/yellow]", default=True):
                console.print("[yellow]Cancelled.[/yellow]")
                return
        
        success = update_package_safely(package, project_path, interactive)
        if success:
            console.print(f"[bold green]✓[/bold green] Package {package} updated successfully!")
        return
    
    # Check outdated packages first
    console.print("[cyan]Checking for outdated packages...[/cyan]\n")
    outdated = check_outdated_packages(project_path)
    
    if not outdated:
        console.print("[bold green]✓[/bold green] All packages are up to date!")
        return
    
    # Show outdated packages
    table = Table(title="Outdated Packages", show_header=True, header_style="bold cyan")
    table.add_column("Package", style="cyan", no_wrap=True)
    table.add_column("Current", style="yellow")
    table.add_column("Latest", style="green")
    
    for pkg in outdated:
        table.add_row(pkg['name'], pkg['current'], pkg['latest'])
    
    console.print(table)
    console.print(f"\n[dim]Found {len(outdated)} outdated package(s)[/dim]\n")
    
    if interactive:
        if not Confirm.ask("[yellow]Proceed with updates?[/yellow]", default=False):
            console.print("[yellow]Cancelled.[/yellow]")
            return
        
        # Update each package with confirmation
        updated = 0
        failed = 0
        
        for pkg in outdated:
            pkg_name = pkg['name']
            if Confirm.ask(f"[cyan]Update {pkg_name}?[/cyan] ({pkg['current']} → {pkg['latest']})", default=True):
                if update_package_safely(pkg_name, project_path, False):
                    updated += 1
                    console.print(f"[green]✓[/green] {pkg_name} updated")
                else:
                    failed += 1
                    console.print(f"[red]✗[/red] {pkg_name} update failed")
        
        console.print(f"\n[bold green]Updated:[/bold green] {updated}")
        if failed > 0:
            console.print(f"[bold red]Failed:[/bold red] {failed}")
    else:
        # Update all without confirmation
        updated = 0
        failed = 0
        
        for pkg in outdated:
            pkg_name = pkg['name']
            if update_package_safely(pkg_name, project_path, False):
                updated += 1
            else:
                failed += 1
        
        console.print(f"\n[bold green]Updated:[/bold green] {updated}")
        if failed > 0:
            console.print(f"[bold red]Failed:[/bold red] {failed}")


@deps.command()
@click.option('--path', '-p', default='.', help='Project path (default: current directory)')
def audit(path):
    """Run security audit on dependencies"""
    project_path = Path(path).resolve()
    
    requirements_file = get_requirements_file(project_path)
    
    if not requirements_file:
        console.print("[bold red]Error:[/bold red] requirements.txt not found. Are you in a Python project?")
        return
    
    console.print("[cyan]Running security audit...[/cyan]")
    console.print("[dim]This may take a while...[/dim]\n")
    
    try:
        vulnerabilities = audit_packages(project_path)
        
        if not vulnerabilities:
            console.print("[bold green]✓[/bold green] No known vulnerabilities found!")
            console.print("\n[yellow]Note:[/yellow] This doesn't guarantee complete security.")
            console.print("Keep your dependencies updated regularly.")
            return
        
        # Group by severity
        severity_counts = {}
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'UNKNOWN')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Display summary
        console.print(Panel(
            f"[bold]Security Audit Results[/bold]\n\n"
            f"Total Vulnerabilities: [red]{len(vulnerabilities)}[/red]\n"
            + "\n".join([f"{sev}: {count}" for sev, count in severity_counts.items()]),
            title="Summary",
            border_style="yellow"
        ))
        
        # Display vulnerabilities table
        table = Table(title="Vulnerabilities", show_header=True, header_style="bold red")
        table.add_column("Package", style="cyan")
        table.add_column("Installed", style="yellow")
        table.add_column("Vulnerability ID", style="red")
        table.add_column("Severity", style="red")
        
        for vuln in vulnerabilities[:20]:  # Show first 20
            table.add_row(
                vuln.get('package', 'N/A'),
                vuln.get('installed', 'N/A'),
                vuln.get('vulnerability', 'N/A'),
                vuln.get('severity', 'UNKNOWN')
            )
        
        console.print("\n")
        console.print(table)
        
        if len(vulnerabilities) > 20:
            console.print(f"\n[dim]... and {len(vulnerabilities) - 20} more[/dim]")
        
        console.print("\n[yellow]Recommendation:[/yellow] Update vulnerable packages using:")
        console.print("  [cyan]projex deps update[/cyan]")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        console.print("\n[yellow]Tip:[/yellow] Install pip-audit manually:")
        console.print("  [cyan]pip install pip-audit[/cyan]")

