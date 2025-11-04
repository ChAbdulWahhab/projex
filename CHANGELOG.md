# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- React/Next.js frontend templates  
- GraphQL templates  
- Kubernetes deployment files  
- Interactive template customization  
- Plugin system for custom templates  

---

## [4.0.0] - 2024-12-XX

### Added - Phase 1: Framework Expansion & Database Support

#### New Framework Templates
- **Bottle** - Micro web framework for small applications
- **Pyramid** - Flexible web framework for large applications
- **Tornado** - Asynchronous web framework and networking library
- **Sanic** - Fast async framework built on uvloop
- **CherryPy** - Minimalist Python web framework

#### Database Support
- Multiple database options: PostgreSQL, MySQL, MongoDB, SQLite, Redis
- Database-specific ORM/ODM configuration
- Database migration setup (Alembic for SQL, custom for NoSQL)
- Docker-compose configurations for each database
- Database-specific environment variables

#### Template Variations
- `minimal` style - Bare minimum setup (no Docker, basic structure)
- `standard` style - Default setup with Docker and tests
- `full` style - Everything included (Docker, tests, CI/CD, docs)

### Added - Phase 2: Developer Experience Enhancements

#### Smart Scaffolding System
- `projex add model` - Generate models with field definitions
- `projex add endpoint` - Generate endpoints with optional CRUD operations
- `projex add service` - Generate service classes (sync/async)
- `projex add middleware` - Generate middleware components
- Framework-aware code generation
- Automatic import management
- Test file generation

#### Authentication Options
- JWT authentication with token-based auth
- OAuth2 authentication (Google, GitHub providers)
- API Key authentication (header/query based)
- Basic authentication (username/password)
- Password hashing with bcrypt
- Login/register endpoints
- Auth examples in README

#### Pre-commit Hooks & Code Quality
- `projex add quality-tools` - Add code quality tools
- Pre-commit hooks configuration
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking
- pylint for advanced linting
- pyproject.toml configuration

#### Project Validation & Info
- `projex validate` - Validate project structure
- `projex info` - Display project information
- `projex doctor` - Alias for validate
- File structure validation
- Dependency checking
- Code statistics (lines of code, files count)
- Git status checking
- Test count and coverage

### Added - Phase 3: DevOps Automation

#### CI/CD Pipeline Generator
- `projex add cicd` - Generate CI/CD configurations
- GitHub Actions support
- GitLab CI support
- CircleCI support
- Test, lint, build stages
- Deployment examples (commented)
- CI badge auto-addition to README

#### Environment Configuration Generator
- `projex env add` - Create environment files
- `projex env list` - List all environment files
- `projex env show` - Show environment variables
- Support for development, staging, production, test environments
- Secure secret key generation
- Database-specific configurations
- Environment variable masking in show command

#### Makefile Generator
- `projex add makefile` - Generate Makefile
- Framework-aware targets
- Common development tasks (install, test, run, docker commands)
- Code quality targets (lint, format)
- Django-specific commands (migrate, superuser)
- Help command

### Added - Phase 4: Additional Features

#### Dependency Management
- `projex deps check` - Check for outdated packages
- `projex deps update` - Update packages safely (interactive)
- `projex deps audit` - Security audit with pip-audit
- Package version tracking
- Requirements.txt auto-update
- Vulnerability reporting

#### Documentation Setup
- `projex add docs --tool mkdocs` - MkDocs documentation setup
- `projex add docs --tool sphinx` - Sphinx documentation setup
- Initial documentation structure
- API documentation templates
- Setup and configuration guides
- Development documentation

#### Testing Enhancements
- `projex add test-config --enhanced` - Enhanced test configuration
- Advanced pytest.ini configuration
- Framework-specific fixtures in conftest.py
- Test data factories pattern
- Coverage configuration (.coveragerc)
- Test markers (slow, integration, unit)
- Example test files

#### Quick Wins
- `--license` option - License selector (MIT, Apache, GPL, BSD, Unlicense)
- `--gitignore` option - Custom gitignore generator using gitignore.io API
- README improvements with badges
- Better structure and organization

### Changed
- Updated CLI to support all new features
- Enhanced project generation with more options
- Improved error handling and user feedback
- Better documentation across all templates

### Fixed
- Version number consistency
- Missing dependencies (requests for gitignore generator)
- CLI command registration

---

## [0.1.0] - 2024-11-03

### Added
- Initial release of **Projex**
- FastAPI template with async support and automatic documentation  
- Django template with Django REST Framework  
- Flask template with Flask-RESTful  
- Interactive CLI with rich terminal output  
- Git initialization support  
- Virtual environment creation  
- Docker and docker-compose configurations  
- pytest setup for all templates  
- Environment variable management  
- Comprehensive documentation  
- Project structure best practices  
- SQLAlchemy/ORM integration  
- JWT authentication setup  
- CORS configuration  
- Requirements management (production and development)  
- Beautiful CLI with progress indicators  
- Template listing command  
- Customizable project metadata (author, description)  

---

### Features by Template

#### FastAPI
- Async/await support  
- Automatic API documentation (Swagger UI)  
- Pydantic models for validation  
- SQLAlchemy ORM integration  
- Alembic migration setup  
- JWT authentication ready  
- CORS middleware  
- Modular API structure (v1 routing)  
- Health check endpoint  
- Sample CRUD endpoints  

#### Django
- Django REST Framework integration  
- Admin panel pre-configured  
- Custom user model ready  
- Django ORM with migrations  
- Environment variable support  
- CORS headers configured  
- pytest-django setup  
- API documentation with drf-spectacular  
- Settings split for different environments  

#### Flask
- Flask-RESTful for API development  
- Flask-SQLAlchemy ORM  
- Flask-Migrate for database migrations  
- Flask-JWT-Extended for authentication  
- Flask-CORS for cross-origin requests  
- Application factory pattern  
- Blueprint-based structure  
- Configuration management  
- Health check endpoint  

---

### Developer Experience
- Rich CLI with colored output  
- Interactive project creation wizard  
- Progress indicators during generation  
- Clear next-step instructions  
- Comprehensive error handling  
- Professional project structure  
- Production-ready configurations  

---

### Documentation
- Detailed README with examples  
- CONTRIBUTING.md for contributors  
- LICENSE file (MIT)  
- Inline code documentation  
- Template-specific documentation  
- Docker usage guide  
- Testing guide  

---

### Testing
- Unit tests for all generators  
- Test fixtures for easy testing  
- Coverage configuration  
- pytest configuration file  
- Sample tests in generated projects  

---

[Unreleased]: https://github.com/ChAbdulWahhab/projex/compare/v0.1.0...HEAD  
[0.1.0]: https://github.com/ChAbdulWahhab/projex/releases/tag/v0.1.0
