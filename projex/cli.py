import click
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from pathlib import Path
import sys

from .generator import ProjectGenerator
from .config import AVAILABLE_TEMPLATES
from .commands.add import add as add_group
from .commands.validate import register_commands
from .commands.env import env as env_group
from .commands.deps import deps as deps_group
from .utils.license_utils import generate_license
from .utils.gitignore_utils import generate_gitignore

console = Console()


def create_gradient_text(text, start_color="#15B248", end_color="#00FF7F"):
    """Create gradient text effect"""
    gradient_text = Text()
    
    # Convert hex to RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    
    # Create gradient for each character
    for i, char in enumerate(text):
        ratio = i / max(len(text) - 1, 1)
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
        gradient_text.append(char, style=f"rgb({r},{g},{b})")
    
    return gradient_text


def print_logo():
    """Print stylized Projex logo"""
    logo = """
    ██████╗ ██████╗  ██████╗      ██╗███████╗██╗  ██╗
    ██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝╚██╗██╔╝
    ██████╔╝██████╔╝██║   ██║     ██║█████╗   ╚███╔╝ 
    ██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝   ██╔██╗ 
    ██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗██╔╝ ██╗
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝╚═╝  ╚═╝
    """
    
    for line in logo.split('\n'):
        gradient_line = create_gradient_text(line)
        console.print(gradient_line)


def create_header():
    """Create styled header with Projex branding"""
    projex_text = create_gradient_text("PROJEX", "#15B248", "#00FF7F")
    
    header = Text()
    header.append("🔨 ")
    header.append(projex_text)
    header.append("\n", style="")
    header.append("Generate production-ready Python projects in seconds", style="dim white")
    
    return Panel(
        header,
        border_style="#15B248",
        padding=(1, 2),
    )


@click.group()
@click.version_option(version="4.0.1", prog_name="Projex")
def main():
    """
    🔨 Projex - Instantly generate Python project boilerplates!
    """
    pass


@main.command()
@click.argument("project_name", required=False)
@click.option(
    "--template",
    "-t",
    type=click.Choice(["fastapi", "django", "flask", "bottle", "pyramid", "tornado", "sanic", "cherrypy"]),
    help="Choose the project template type",
)
@click.option("--path", "-p", default=".", help="Directory path to create the project")
@click.option("--author", "-a", help="Author name")
@click.option("--description", "-d", help="Project description")
@click.option(
    "--db",
    type=click.Choice(["postgresql", "mysql", "mongodb", "sqlite", "redis"]),
    default="postgresql",
    help="Database type (default: postgresql)",
)
@click.option(
    "--style",
    type=click.Choice(["minimal", "standard", "full"]),
    default="standard",
    help="Template style: minimal (bare minimum), standard (default), full (everything)",
)
@click.option(
    "--auth",
    type=click.Choice(["jwt", "oauth2", "apikey", "basic"]),
    help="Authentication method (jwt, oauth2, apikey, basic)",
)
@click.option("--no-git", is_flag=True, help="Skip git initialization")
@click.option("--no-venv", is_flag=True, help="Skip virtual environment creation")
@click.option(
    "--license",
    type=click.Choice(["mit", "apache", "gpl", "bsd", "unlicense"]),
    help="License type (mit, apache, gpl, bsd, unlicense)",
)
@click.option(
    "--gitignore",
    help="Comma-separated gitignore templates (e.g., python,venv,pycharm,vscode)",
)
def create(project_name, template, path, author, description, db, style, auth, no_git, no_venv, license, gitignore):
    """Create a new Python project using Projex templates."""

    print_logo()
    console.print()

    # Interactive mode if not provided via CLI
    if not project_name:
        projex_colored = Text()
        projex_colored.append("Project name", style="#15B248 bold")
        project_name = Prompt.ask(projex_colored)

    if not template:
        console.print("\n")
        template_header = Text("Available Templates:", style="#15B248 bold")
        console.print(template_header)
        console.print()
        
        for i, (key, value) in enumerate(AVAILABLE_TEMPLATES.items(), 1):
            template_text = Text()
            template_text.append(f"  {i}. ", style="white")
            template_text.append(key, style="#15B248 bold")
            template_text.append(f" - {value['description']}", style="dim white")
            console.print(template_text)

        prompt_text = Text()
        prompt_text.append("\nChoose template", style="#15B248 bold")
        
        template_choice = Prompt.ask(prompt_text, default="1")

        template_map = {
            "1": "fastapi", 
            "2": "django", 
            "3": "flask",
            "4": "bottle",
            "5": "pyramid",
            "6": "tornado",
            "7": "sanic",
            "8": "cherrypy"
        }
        template = template_map.get(template_choice, template_choice)

    if not author:
        author_prompt = Text("Author name", style="#15B248 bold")
        author = Prompt.ask(author_prompt, default="Developer")

    if not description:
        desc_prompt = Text("Project description", style="#15B248 bold")
        description = Prompt.ask(
            desc_prompt,
            default=f"A {template} project generated by Projex",
        )

    # Database selection
    if not template:
        console.print("\n")
        db_header = Text("Available Databases:", style="#15B248 bold")
        console.print(db_header)
        console.print()
        
        databases = ["postgresql", "mysql", "mongodb", "sqlite", "redis"]
        for i, db_name in enumerate(databases, 1):
            db_text = Text()
            db_text.append(f"  {i}. ", style="white")
            db_text.append(db_name, style="#15B248 bold")
            console.print(db_text)
        
        db_prompt = Text("\nChoose database", style="#15B248 bold")
        db_choice = Prompt.ask(db_prompt, default="1")
        
        db_map = {
            "1": "postgresql",
            "2": "mysql",
            "3": "mongodb",
            "4": "sqlite",
            "5": "redis"
        }
        db = db_map.get(db_choice, db_choice)

    # Show summary with styled output
    console.print()
    summary_header = Text("Project Configuration:", style="#15B248 bold")
    console.print(summary_header)
    
    def print_config_line(label, value):
        line = Text()
        line.append(f"  {label}: ", style="white")
        line.append(str(value), style="#15B248")
        console.print(line)
    
    print_config_line("Name", project_name)
    print_config_line("Template", template)
    print_config_line("Database", db)
    print_config_line("Style", style)
    if auth:
        print_config_line("Authentication", auth)
    print_config_line("Path", Path(path).absolute() / project_name)
    print_config_line("Author", author)
    print_config_line("Git Init", 'No' if no_git else 'Yes')
    print_config_line("Virtual Env", 'No' if no_venv else 'Yes')

    confirm_text = Text("\nProceed with project creation?", style="#15B248 bold")
    if not Confirm.ask(confirm_text, default=True):
        console.print(Text("Cancelled by user.", style="yellow"))
        return

    # Project generation logic
    try:
        generator = ProjectGenerator(
            project_name=project_name,
            template_type=template,
            base_path=path,
            author=author,
            description=description,
            database=db,
            style=style,
            auth=auth,
            init_git=not no_git,
            create_venv=not no_venv,
        )

        with Progress(
            SpinnerColumn(spinner_name="dots", style="#15B248"),
            TextColumn("[#15B248]{task.description}[/#15B248]"),
            console=console,
        ) as progress:
            task = progress.add_task("Creating project...", total=None)
            project_path = generator.generate()
            progress.update(task, completed=True)

        success_text = Text()
        success_text.append("\n✓ ", style="bold #15B248")
        success_text.append("Project created successfully at: ", style="white")
        success_text.append(str(project_path), style="#15B248 bold")
        console.print(success_text)
        
        # Post-generation: Add license if specified
        if license:
            try:
                license_file = generate_license(project_path, license, author)
                lic_text = Text()
                lic_text.append("✓ ", style="#15B248")
                lic_text.append(f"License file created: {license_file.name}", style="white")
                console.print(lic_text)
            except Exception as e:
                console.print(Text(f"Warning: Could not create license: {str(e)}", style="yellow"))
        
        # Post-generation: Add custom gitignore if specified
        if gitignore:
            try:
                templates = [t.strip() for t in gitignore.split(',')]
                gitignore_file = generate_gitignore(project_path, templates)
                git_text = Text()
                git_text.append("✓ ", style="#15B248")
                git_text.append("Custom .gitignore created", style="white")
                console.print(git_text)
            except Exception as e:
                console.print(Text(f"Warning: Could not create custom gitignore: {str(e)}", style="yellow"))

        # Post-creation guidance with styled output
        console.print()
        steps_header = Text("Next Steps:", style="#15B248 bold")
        console.print(steps_header)
        
        def print_step(step_text):
            step = Text()
            step.append("  ", style="white")
            step.append(step_text, style="white")
            console.print(step)
        
        print_step(f"cd {project_name}")
        if not no_venv:
            print_step("source venv/bin/activate  # (Windows: venv\\Scripts\\activate)")
        print_step("pip install -r requirements.txt")

        if template == "fastapi":
            print_step("uvicorn app.main:app --reload")
        elif template == "django":
            print_step("python manage.py migrate")
            print_step("python manage.py runserver")
        elif template == "flask":
            print_step("python run.py")
        elif template == "bottle":
            print_step("python app/main.py")
        elif template == "pyramid":
            print_step("python run.py")
        elif template == "tornado":
            print_step("python app/main.py")
        elif template == "sanic":
            print_step("python app/main.py")
        elif template == "cherrypy":
            print_step("python app/main.py")

    except Exception as e:
        error_text = Text()
        error_text.append("✗ Error: ", style="bold red")
        error_text.append(str(e), style="red")
        console.print(error_text)
        sys.exit(1)


@main.command()
def list():
    """List all available Projex templates."""
    
    console.print()
    header = Text("Available Templates:", style="#15B248 bold")
    console.print(header)
    console.print()

    for name, details in AVAILABLE_TEMPLATES.items():
        title = Text(name.upper(), style="#15B248 bold")
        
        content = Text()
        content.append(details['description'], style="white bold")
        content.append("\n", style="")
        content.append("Features: ", style="dim white")
        content.append(', '.join(details['features']), style="dim white")
        
        console.print(
            Panel(
                content,
                title=title,
                border_style="#15B248",
                padding=(1, 2),
            )
        )


# Register add command group
main.add_command(add_group)

# Register env command group
main.add_command(env_group)

# Register deps command group
main.add_command(deps_group)

# Register validation and info commands
register_commands(main)


if __name__ == "__main__":
    main()