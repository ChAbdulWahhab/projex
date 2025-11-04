@echo off
REM Git Commits for Release 4.0.0 (Windows Batch)
REM Run these commands in sequence

echo Starting git commits for Release 4.0.0...

REM Commit 1: Phase 1 - Framework templates
git add projex/generator.py projex/config.py projex/cli.py
git commit -m "feat: add 5 new framework templates (Bottle, Pyramid, Tornado, Sanic, CherryPy)" -m "- Add _generate_bottle() method with complete project structure" -m "- Add _generate_pyramid() method with flexible architecture" -m "- Add _generate_tornado() method with async support" -m "- Add _generate_sanic() method with high-performance async" -m "- Add _generate_cherrypy() method with minimalist design" -m "- Update CLI to include all 8 framework options" -m "- Update config.py with template definitions and dependencies" -m "- All templates include Docker, tests, and best practices"

REM Commit 2: Phase 1 - Database support
git add projex/generator.py projex/cli.py
git commit -m "feat: add multiple database support (PostgreSQL, MySQL, MongoDB, SQLite, Redis)" -m "- Add --db flag to CLI with 5 database options" -m "- Implement _setup_database() method with DB-specific configs" -m "- Generate appropriate ORM/ODM for each database type" -m "- Update docker-compose.yml templates for each database" -m "- Add database migration setup (Alembic for SQL, custom for NoSQL)" -m "- Update .env.example with database-specific variables" -m "- Framework-aware database configuration"

REM Commit 3: Phase 1 - Template styles
git add projex/generator.py projex/cli.py
git commit -m "feat: add template style variations (minimal, standard, full)" -m "- Add --style flag to CLI with 3 style options" -m "- Implement conditional logic in generator methods" -m "- Minimal style: bare minimum setup without Docker" -m "- Standard style: default setup with Docker and tests" -m "- Full style: everything included (Docker, tests, CI/CD, docs)" -m "- Style-aware file generation"

REM Commit 4: Phase 2 - Smart scaffolding
git add projex/commands/add.py projex/utils/codegen.py projex/utils/detector.py projex/cli.py
git commit -m "feat: add smart scaffolding system for code generation" -m "- Add projex add model command with field definitions" -m "- Add projex add endpoint command with CRUD support" -m "- Add projex add service command (sync/async)" -m "- Add projex add middleware command" -m "- Implement framework auto-detection" -m "- Generate framework-aware code with proper imports" -m "- Create codegen.py with code generation utilities" -m "- Add detector.py for framework detection"

REM Commit 5: Phase 2 - Authentication
git add projex/generator.py projex/cli.py
git commit -m "feat: add multiple authentication methods (JWT, OAuth2, API Key, Basic)" -m "- Add --auth flag to CLI with 4 auth options" -m "- Implement _setup_jwt_auth() method" -m "- Implement _setup_oauth2_auth() method" -m "- Implement _setup_apikey_auth() method" -m "- Implement _setup_basic_auth() method" -m "- Generate auth middleware/decorators per framework" -m "- Add login/register endpoints" -m "- Include password hashing with bcrypt" -m "- Add authentication examples in README"

REM Commit 6: Phase 2 - Quality tools
git add projex/commands/add.py projex/utils/quality_tools.py
git commit -m "feat: add pre-commit hooks and code quality tools" -m "- Add projex add quality-tools command" -m "- Generate .pre-commit-config.yaml with hooks" -m "- Create pyproject.toml with tool configurations" -m "- Add black, isort, flake8, mypy, pylint support" -m "- Update requirements-dev.txt with quality packages" -m "- Generate GitHub Actions workflow for CI checks" -m "- Add quality_tools.py utility"

REM Commit 7: Phase 2 - Validation and Info
git add projex/commands/validate.py projex/cli.py
git commit -m "feat: add project validation and info commands" -m "- Add projex validate command for structure validation" -m "- Add projex info command for project statistics" -m "- Add projex doctor command (alias for validate)" -m "- Implement file structure validation" -m "- Implement dependency checking" -m "- Add code statistics (lines, files count)" -m "- Add git status checking" -m "- Add test count and coverage detection" -m "- Create validate.py with validation utilities"

REM Commit 8: Phase 3 - CI/CD
git add projex/commands/add.py projex/utils/cicd.py
git commit -m "feat: add CI/CD pipeline generator (GitHub Actions, GitLab CI, CircleCI)" -m "- Add projex add cicd command with provider selection" -m "- Generate GitHub Actions workflow (.github/workflows/ci.yml)" -m "- Generate GitLab CI configuration (.gitlab-ci.yml)" -m "- Generate CircleCI configuration (.circleci/config.yml)" -m "- Include test, lint, build stages" -m "- Add deployment examples (commented)" -m "- Auto-add CI badges to README" -m "- Create cicd.py utility"

REM Commit 9: Phase 3 - Environment management
git add projex/commands/env.py projex/utils/env_utils.py projex/cli.py
git commit -m "feat: add environment configuration generator" -m "- Add projex env command group" -m "- Add projex env add command for creating env files" -m "- Add projex env list command for listing env files" -m "- Add projex env show command for viewing variables" -m "- Support development, staging, production, test environments" -m "- Generate secure secret keys" -m "- Framework and database-aware configurations" -m "- Mask sensitive values in show command" -m "- Create env.py command and env_utils.py utility"

REM Commit 10: Phase 3 - Makefile
git add projex/commands/add.py projex/utils/makefile_utils.py
git commit -m "feat: add Makefile generator with common development tasks" -m "- Add projex add makefile command" -m "- Generate framework-aware Makefile targets" -m "- Include install, test, run, docker commands" -m "- Add lint and format targets" -m "- Django-specific commands (migrate, superuser)" -m "- Help command with usage instructions" -m "- Create makefile_utils.py utility"

REM Commit 11: Phase 4 - Dependency management
git add projex/commands/deps.py projex/utils/deps_utils.py projex/cli.py
git commit -m "feat: add dependency management commands" -m "- Add projex deps command group" -m "- Add projex deps check for outdated packages" -m "- Add projex deps update for safe package updates" -m "- Add projex deps audit for security scanning" -m "- Interactive update mode with confirmations" -m "- Auto-update requirements.txt" -m "- Vulnerability reporting with pip-audit" -m "- Create deps.py command and deps_utils.py utility"

REM Commit 12: Phase 4 - Documentation
git add projex/commands/add.py projex/utils/docs_utils.py
git commit -m "feat: add documentation setup (MkDocs and Sphinx)" -m "- Add projex add docs command with tool selection" -m "- Generate MkDocs setup with Material theme" -m "- Generate Sphinx setup with RTD theme" -m "- Create initial documentation structure" -m "- Add API documentation templates" -m "- Add setup and configuration guides" -m "- Auto-update requirements-dev.txt" -m "- Create docs_utils.py utility"

REM Commit 13: Phase 4 - Testing enhancements
git add projex/commands/add.py projex/utils/test_utils.py
git commit -m "feat: add enhanced testing configuration" -m "- Add projex add test-config --enhanced command" -m "- Generate advanced pytest.ini configuration" -m "- Create conftest.py with framework-specific fixtures" -m "- Add test data factories pattern" -m "- Generate .coveragerc for coverage configuration" -m "- Add test markers (slow, integration, unit)" -m "- Include example test files" -m "- Create test_utils.py utility"

REM Commit 14: Phase 4 - License and gitignore
git add projex/utils/license_utils.py projex/utils/gitignore_utils.py projex/cli.py
git commit -m "feat: add license selector and gitignore generator" -m "- Add --license flag to create command (MIT, Apache, GPL, BSD, Unlicense)" -m "- Add --gitignore flag to create command with templates" -m "- Use gitignore.io API for custom gitignore generation" -m "- Generate license files with proper copyright" -m "- Post-generation license and gitignore handling" -m "- Create license_utils.py and gitignore_utils.py utilities"

REM Commit 15: Documentation updates
git add README.md QUICKSTART.md EXAMPLES.md
git commit -m "docs: update documentation for Release 4.0.0" -m "- Update README.md with all new features and commands" -m "- Update QUICKSTART.md with advanced features section" -m "- Update EXAMPLES.md with comprehensive examples" -m "- Add use cases and workflows" -m "- Document all CLI commands and options" -m "- Add badges and better structure"

REM Commit 16: CHANGELOG update
git add CHANGELOG.md
git commit -m "docs: update CHANGELOG.md for Release 4.0.0" -m "- Add comprehensive Release 4.0.0 changelog" -m "- Document all Phase 1-4 features" -m "- List all new commands and utilities" -m "- Organize by phases and features"

REM Commit 17: Version bump and dependencies
git add projex/__init__.py projex/cli.py setup.py requirements.txt projex/utils/quality_tools.py
git commit -m "chore: bump version to 4.0.0 and update dependencies" -m "- Update version to 4.0.0 in __init__.py, cli.py, setup.py" -m "- Add requests>=2.31.0 dependency for gitignore generator" -m "- Update rich version to >=13.0.0" -m "- Update setup.py with all dependencies" -m "- Fix quality_tools.py indentation issue"

REM Commit 18: Final preparation
git add .gitignore
git commit -m "chore: final Release 4.0.0 preparation" -m "- Update .gitignore with PyPI credentials" -m "- Verify all imports and syntax" -m "- Ensure all commands are properly registered" -m "- Final code quality checks" -m "- Ready for PyPI release"

echo.
echo All commits completed! Ready for push.
echo.
echo To push to remote:
echo   git push origin main
pause

