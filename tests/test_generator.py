import pytest
import shutil
from pathlib import Path
from projex.generator import ProjectGenerator


@pytest.fixture
def temp_dir(tmp_path):
    """Fixture for temporary directory"""
    yield tmp_path
    # Cleanup
    if tmp_path.exists():
        shutil.rmtree(tmp_path)


def test_fastapi_generation(temp_dir):
    """Test FastAPI project generation"""
    generator = ProjectGenerator(
        project_name="test_fastapi",
        template_type="fastapi",
        base_path=str(temp_dir),
        author="Test Author",
        description="Test FastAPI project",
        init_git=False,
        create_venv=False
    )
    
    project_path = generator.generate()
    
    # Check if project directory was created
    assert project_path.exists()
    assert project_path.is_dir()
    
    # Check key files exist
    assert (project_path / "app" / "main.py").exists()
    assert (project_path / "app" / "core" / "config.py").exists()
    assert (project_path / "requirements.txt").exists()
    assert (project_path / "README.md").exists()
    assert (project_path / ".gitignore").exists()
    assert (project_path / "Dockerfile").exists()
    assert (project_path / "docker-compose.yml").exists()
    
    # Check app structure
    assert (project_path / "app" / "api" / "v1" / "router.py").exists()
    assert (project_path / "app" / "models").exists()
    assert (project_path / "app" / "schemas").exists()
    
    # Check tests
    assert (project_path / "tests" / "test_main.py").exists()


def test_django_generation(temp_dir):
    """Test Django project generation"""
    generator = ProjectGenerator(
        project_name="test_django",
        template_type="django",
        base_path=str(temp_dir),
        author="Test Author",
        description="Test Django project",
        init_git=False,
        create_venv=False
    )
    
    project_path = generator.generate()
    
    # Check if project directory was created
    assert project_path.exists()
    
    # Check key files exist
    assert (project_path / "manage.py").exists()
    assert (project_path / "config" / "settings.py").exists()
    assert (project_path / "config" / "urls.py").exists()
    assert (project_path / "requirements.txt").exists()
    
    # Check apps structure
    assert (project_path / "apps" / "core" / "models.py").exists()
    assert (project_path / "apps" / "core" / "views.py").exists()
    assert (project_path / "apps" / "core" / "tests.py").exists()


def test_flask_generation(temp_dir):
    """Test Flask project generation"""
    generator = ProjectGenerator(
        project_name="test_flask",
        template_type="flask",
        base_path=str(temp_dir),
        author="Test Author",
        description="Test Flask project",
        init_git=False,
        create_venv=False
    )
    
    project_path = generator.generate()
    
    # Check if project directory was created
    assert project_path.exists()
    
    # Check key files exist
    assert (project_path / "run.py").exists()
    assert (project_path / "app" / "__init__.py").exists()
    assert (project_path / "app" / "config.py").exists()
    assert (project_path / "requirements.txt").exists()
    
    # Check app structure
    assert (project_path / "app" / "api" / "routes.py").exists()
    assert (project_path / "app" / "models").exists()
    
    # Check tests
    assert (project_path / "tests" / "test_api.py").exists()


def test_project_already_exists(temp_dir):
    """Test error handling when project directory already exists"""
    project_name = "existing_project"
    (temp_dir / project_name).mkdir()
    
    generator = ProjectGenerator(
        project_name=project_name,
        template_type="fastapi",
        base_path=str(temp_dir),
        init_git=False,
        create_venv=False
    )
    
    with pytest.raises(FileExistsError):
        generator.generate()


def test_requirements_files(temp_dir):
    """Test requirements files are created correctly"""
    generator = ProjectGenerator(
        project_name="test_requirements",
        template_type="fastapi",
        base_path=str(temp_dir),
        init_git=False,
        create_venv=False
    )
    
    project_path = generator.generate()
    
    # Check requirements files exist
    assert (project_path / "requirements.txt").exists()
    assert (project_path / "requirements-dev.txt").exists()
    
    # Check content
    req_content = (project_path / "requirements.txt").read_text()
    assert "fastapi" in req_content
    assert "uvicorn" in req_content
    
    dev_req_content = (project_path / "requirements-dev.txt").read_text()
    assert "-r requirements.txt" in dev_req_content
    assert "pytest" in dev_req_content


def test_env_file(temp_dir):
    """Test .env.example file is created"""
    generator = ProjectGenerator(
        project_name="test_env",
        template_type="fastapi",
        base_path=str(temp_dir),
        init_git=False,
        create_venv=False
    )
    
    project_path = generator.generate()
    
    env_file = project_path / ".env.example"
    assert env_file.exists()
    
    content = env_file.read_text()
    assert "DATABASE_URL" in content
    assert "SECRET_KEY" in content
    assert "DEBUG" in content


def test_docker_files(temp_dir):
    """Test Docker files are created"""
    generator = ProjectGenerator(
        project_name="test_docker",
        template_type="fastapi",
        base_path=str(temp_dir),
        init_git=False,
        create_venv=False
    )
    
    project_path = generator.generate()
    
    # Check Dockerfile
    dockerfile = project_path / "Dockerfile"
    assert dockerfile.exists()
    content = dockerfile.read_text()
    assert "FROM python" in content
    assert "COPY requirements.txt" in content
    
    # Check docker-compose
    compose_file = project_path / "docker-compose.yml"
    assert compose_file.exists()
    content = compose_file.read_text()
    assert "services:" in content
    assert "web:" in content
    assert "db:" in content


def test_readme_customization(temp_dir):
    """Test README is customized with project details"""
    project_name = "my_custom_project"
    author = "John Doe"
    description = "My awesome project"
    
    generator = ProjectGenerator(
        project_name=project_name,
        template_type="fastapi",
        base_path=str(temp_dir),
        author=author,
        description=description,
        init_git=False,
        create_venv=False
    )
    
    project_path = generator.generate()
    
    readme = project_path / "README.md"
    content = readme.read_text()
    
    assert project_name in content
    assert author in content
    assert description in content