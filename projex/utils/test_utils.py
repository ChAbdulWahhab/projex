"""Testing utilities"""
from pathlib import Path
from typing import Optional


def generate_enhanced_test_config(project_path: Path, framework: Optional[str] = None) -> Path:
    """
    Generate enhanced pytest configuration.
    
    Args:
        project_path: Path to project root
        framework: Detected framework name
        
    Returns:
        Path to created pytest.ini
    """
    # Generate pytest.ini
    pytest_config = """[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-report=xml
    --cov-fail-under=80
markers =
    slow: marks tests as slow (deselect with '-m \"not slow\"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
"""
    
    pytest_file = project_path / 'pytest.ini'
    pytest_file.write_text(pytest_config)
    
    # Generate conftest.py
    tests_dir = project_path / 'tests'
    tests_dir.mkdir(exist_ok=True)
    
    conftest_content = """\"\"\"Pytest configuration and fixtures\"\"\"
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_data():
    \"\"\"Sample data fixture\"\"\"
    return {
        'name': 'Test',
        'value': 42
    }


@pytest.fixture
def mock_request():
    \"\"\"Mock request fixture\"\"\"
    class MockRequest:
        def __init__(self):
            self.headers = {}
            self.json_data = {}
        
        def json(self):
            return self.json_data
    
    return MockRequest()


# Framework-specific fixtures
"""
    
    # Add framework-specific fixtures
    if framework == 'django':
        conftest_content += """
@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    \"\"\"Django database setup\"\"\"
    pass


@pytest.fixture
def api_client():
    \"\"\"Django REST Framework API client\"\"\"
    from rest_framework.test import APIClient
    return APIClient()
"""
    elif framework == 'fastapi':
        conftest_content += """
@pytest.fixture
def client():
    \"\"\"FastAPI test client\"\"\"
    from app.main import app
    from fastapi.testclient import TestClient
    return TestClient(app)
"""
    elif framework == 'flask':
        conftest_content += """
@pytest.fixture
def client():
    \"\"\"Flask test client\"\"\"
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
"""
    
    conftest_file = tests_dir / 'conftest.py'
    
    # Append if exists, otherwise create
    if conftest_file.exists():
        existing = conftest_file.read_text()
        # Only add if fixtures not already present
        if 'sample_data' not in existing:
            conftest_file.write_text(existing + '\n' + conftest_content.split('# Framework-specific fixtures')[1])
    else:
        conftest_file.write_text(conftest_content)
    
    # Create fixtures directory
    fixtures_dir = tests_dir / 'fixtures'
    fixtures_dir.mkdir(exist_ok=True)
    
    # Create example factory
    factory_content = """\"\"\"Test data factories\"\"\"
# Example factory pattern for creating test data

def create_user(**kwargs):
    \"\"\"Create a test user\"\"\"
    defaults = {
        'name': 'Test User',
        'email': 'test@example.com',
        'is_active': True
    }
    defaults.update(kwargs)
    return defaults


def create_item(**kwargs):
    \"\"\"Create a test item\"\"\"
    defaults = {
        'name': 'Test Item',
        'value': 100
    }
    defaults.update(kwargs)
    return defaults
"""
    (fixtures_dir / 'factories.py').write_text(factory_content)
    
    # Create example test with mocks
    example_test = tests_dir / 'test_example.py'
    if not example_test.exists():
        example_content = """\"\"\"Example test file with common patterns\"\"\"
import pytest
from unittest.mock import Mock, patch


def test_example(sample_data):
    \"\"\"Example test using fixture\"\"\"
    assert sample_data['name'] == 'Test'
    assert sample_data['value'] == 42


@pytest.mark.unit
def test_unit_example():
    \"\"\"Example unit test\"\"\"
    assert 1 + 1 == 2


@pytest.mark.slow
def test_slow_example():
    \"\"\"Example slow test\"\"\"
    # This test would be skipped with: pytest -m "not slow"
    pass


@patch('app.utils.external_api')
def test_with_mock(mock_api):
    \"\"\"Example test with mocking\"\"\"
    mock_api.return_value = {'status': 'ok'}
    # Your test code here
    assert mock_api()['status'] == 'ok'
"""
        example_test.write_text(example_content)
    
    # Create .coveragerc
    coverage_config = """[run]
source = app
omit = 
    */tests/*
    */migrations/*
    */venv/*
    */env/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
"""
    coverage_file = project_path / '.coveragerc'
    coverage_file.write_text(coverage_config)
    
    return pytest_file

