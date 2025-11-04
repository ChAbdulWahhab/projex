# Quick Start

Get up and running with Projex in under 5 minutes!

## Installation

```bash
pip install projex
```

## Create Your First Project

### Interactive Mode (Easiest)

```bash
projex create
```

The CLI will ask you:

1. **Project name?** → Enter your project name
2. **Framework?** → Choose from 8 options
3. **Database?** → Select database type
4. **Authentication?** → Pick auth method
5. **Template style?** → Choose minimal/standard/full

### Command Line Mode

```bash
projex create my-api --template fastapi --db postgresql --auth jwt
```

## Start Development

### FastAPI Example

```bash
# Navigate to project
cd my-api

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for API documentation!

### Django Example

```bash
cd my-site
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit [http://localhost:8000/admin](http://localhost:8000/admin)

### Flask Example

```bash
cd my-app
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Visit [http://localhost:5000](http://localhost:5000)

## What You Get

Every project includes:

✅ Complete project structure  
✅ Docker & docker-compose  
✅ Testing setup (pytest)  
✅ Environment configuration  
✅ Database integration  
✅ Authentication (if selected)  
✅ Git initialization  
✅ Best practices  

## Common Commands

```bash
# List available templates
projex list

# Get help
projex --help
projex create --help

# Skip options
projex create my-app --template flask --no-git --no-venv
```

## Next Steps

### Add Components

```bash
# Add a model
projex add model User --fields name:str,email:str

# Add CRUD endpoint
projex add endpoint users --crud

# Add CI/CD
projex add cicd --provider github
```

### Environment Setup

```bash
# Create environment files
projex env add development
projex env add production

# Copy example env
cp .env.example .env
# Edit .env with your values
```

### Docker

```bash
# Start with docker-compose
docker-compose up --build
```

## Tips

💡 Use `--style minimal` for learning  
💡 Use `--style full` for production  
💡 Check generated README.md for project-specific instructions  
💡 Run tests from day one: `pytest`  

## Troubleshooting

### Port Already in Use

```bash
# FastAPI
uvicorn app.main:app --port 8001

# Django
python manage.py runserver 8001

# Flask
flask run --port 5001
```

### Import Errors

```bash
# Ensure virtual environment is active
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## Learn More

- [Framework Templates](../templates/overview.md)
- [CLI Reference](../cli/create.md)
- [Features Overview](../features/scaffolding.md)