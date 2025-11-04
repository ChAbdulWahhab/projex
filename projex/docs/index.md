# Welcome to Projex Documentation

<div>
  <h1>🔨 Projex</h1>
  <p><strong>A powerful CLI tool to generate production-ready Python project boilerplates instantly</strong></p>
  
  <p>
    <a href="https://pypi.org/project/projex/"><img src="https://img.shields.io/pypi/v/projex.svg" alt="PyPI version"></a>
    <a href="https://pypi.org/project/projex/"><img src="https://img.shields.io/pypi/pyversions/projex.svg" alt="Python versions"></a>
    <a href="https://github.com/ChAbdulWahhab/projex/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"></a>
    <a href="https://github.com/ChAbdulWahhab/projex"><img src="https://img.shields.io/github/stars/ChAbdulWahhab/projex.svg" alt="GitHub stars"></a>
  </p>
</div>

---

## Why Projex?

Skip the boring setup and jump straight into coding! Projex generates complete, production-ready project structures with best practices baked in.

### ⚡ Quick Example

```bash
# Install
pip install projex

# Create your project
projex create my-api --template fastapi --db postgresql --auth jwt

# Start coding!
cd my-api
source venv/bin/activate
uvicorn app.main:app --reload
```

That's it! You now have a production-ready FastAPI project with PostgreSQL and JWT authentication! 🚀

---

## ✨ Key Features

<div class="grid cards" markdown>

-   :rocket:{ .lg .middle } **8 Framework Templates**

    ---

    FastAPI, Django, Flask, Bottle, Pyramid, Tornado, Sanic, CherryPy

    [:octicons-arrow-right-24: View Templates](templates/overview.md)

-   :material-database:{ .lg .middle } **5 Database Options**

    ---

    PostgreSQL, MySQL, MongoDB, SQLite, Redis

    [:octicons-arrow-right-24: Learn More](features/databases.md)

-   :material-shield-lock:{ .lg .middle } **4 Auth Methods**

    ---

    JWT, OAuth2, API Key, Basic Authentication

    [:octicons-arrow-right-24: Authentication Guide](features/authentication.md)

-   :material-code-braces:{ .lg .middle } **Smart Scaffolding**

    ---

    Generate models, endpoints, services with one command

    [:octicons-arrow-right-24: Scaffolding Docs](features/scaffolding.md)

-   :material-docker:{ .lg .middle } **Docker Ready**

    ---

    Complete Docker and docker-compose setup included

    [:octicons-arrow-right-24: Docker Guide](advanced/best-practices.md#docker)

-   :material-test-tube:{ .lg .middle } **Testing Built-in**

    ---

    pytest configuration with fixtures and examples

    [:octicons-arrow-right-24: Testing Guide](features/testing.md)

-   :octicons-workflow-24:{ .lg .middle } **CI/CD Pipelines**

    ---

    GitHub Actions, GitLab CI, CircleCI configs

    [:octicons-arrow-right-24: CI/CD Setup](features/cicd.md)

-   :material-file-document:{ .lg .middle } **Documentation Tools**

    ---

    MkDocs and Sphinx setup included

    [:octicons-arrow-right-24: Docs Setup](features/docs-setup.md)

</div>

---

## 🚀 Quick Start

Get started in 3 easy steps:

### 1. Install Projex

=== "pip"
    ```bash
    pip install projex
    ```

=== "From Source"
    ```bash
    git clone https://github.com/ChAbdulWahhab/projex.git
    cd projex
    pip install -e .
    ```

### 2. Create Your Project

=== "Interactive Mode"
    ```bash
    projex create
    ```
    The CLI will guide you through the setup with interactive prompts.

=== "Command Line"
    ```bash
    projex create my-api --template fastapi --db postgresql
    ```

### 3. Start Development

```bash
cd my-api
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation! 📚

---

## 📋 What Gets Generated?

Every project includes:

✅ **Production-ready structure** - Best practices baked in  
✅ **Docker support** - Dockerfile and docker-compose  
✅ **Testing setup** - pytest with examples  
✅ **Environment config** - .env file management  
✅ **Database integration** - ORM/ODM configured  
✅ **Authentication** - Ready to use auth system  
✅ **API documentation** - Auto-generated docs  
✅ **Git initialization** - Ready for version control  

---

## 🎯 Use Cases

### Microservices Architecture
```bash
projex create user-service --template fastapi
projex create order-service --template fastapi
projex create payment-service --template fastapi
```
[Learn more about microservices →](use-cases/microservices.md)

### REST API Development
```bash
projex create my-api --template fastapi --db postgresql --auth jwt
cd my-api
projex add cicd --provider github
```
[REST API guide →](use-cases/rest-api.md)

### Full-Stack Application
```bash
projex create backend --template fastapi
projex create admin --template django
```
[Full-stack setup →](use-cases/fullstack.md)

---

## 📚 Next Steps

<div class="grid cards" markdown>

-   [:material-clock-fast:{ .lg } **Quick Start Guide**](getting-started/quickstart.md)
    
    Learn the basics in 5 minutes

-   [:material-view-grid:{ .lg } **Framework Templates**](templates/overview.md)
    
    Explore all 8 framework options

-   [:material-hammer-wrench:{ .lg } **CLI Reference**](cli/create.md)
    
    Complete command documentation

-   [:material-school:{ .lg } **Advanced Topics**](advanced/custom-templates.md)
    
    Customization and best practices

</div>

---

## 🤝 Community & Support

- **GitHub:** [Star the repository](https://github.com/ChAbdulWahhab/projex) ⭐
- **Issues:** [Report bugs](https://github.com/ChAbdulWahhab/projex/issues) 🐛
- **Discussions:** [Ask questions](https://github.com/ChAbdulWahhab/projex/discussions) 💬
- **Contributing:** [Contribution guidelines](contributing/guidelines.md) 🤝

---

## 🗺️ Roadmap

Check out our [Changelog](changelog.md) for recent updates and the [GitHub Projects](https://github.com/ChAbdulWahhab/projex/projects) for upcoming features.

### Recently Added ✅
- 8 framework templates
- Smart scaffolding system
- CI/CD pipeline generation
- Environment management
- Enhanced testing tools

### Coming Soon 🚀
- Frontend templates (React, Vue)
- GraphQL support
- Kubernetes configurations
- Plugin system

---

<div align="center">
  <p><strong>Made with ❤️ by developers, for developers</strong></p>
  <p>
    <a href="https://github.com/ChAbdulWahhab">GitHub</a> •
    <a href="https://pypi.org/project/projex/">PyPI</a> •
    <a href="https://twitter.com/projex_cli">Twitter</a>
  </p>
</div>