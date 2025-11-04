# Your First Project

Let's build a complete REST API from scratch using Projex!

## What We'll Build

A **User Management API** with:
- User CRUD operations
- JWT authentication
- PostgreSQL database
- Docker support
- Tests

## Step 1: Create Project

```bash
projex create user-api \
  --template fastapi \
  --db postgresql \
  --auth jwt \
  --style full \
  --author "Your Name"
```

**What happens:**
- Creates `user-api/` directory
- Generates complete project structure
- Sets up virtual environment
- Initializes git repository
- Installs dependencies

## Step 2: Explore Structure

```bash
cd user-api
tree -L 2
```

You'll see:
```
user-api/
├── app/
│   ├── main.py          # Application entry
│   ├── core/            # Config & database
│   ├── api/             # API routes
│   ├── models/          # Database models
│   └── schemas/         # Pydantic schemas
├── tests/               # Test files
├── .env.example         # Environment template
├── Dockerfile           # Docker config
├── docker-compose.yml   # Docker services
├── requirements.txt     # Dependencies
└── README.md            # Project docs
```

## Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your values
nano .env  # or use any editor
```

Example `.env`:
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/userdb
SECRET_KEY=your-secret-key-here
DEBUG=True
ENVIRONMENT=development
```

## Step 4: Start Database

### Using Docker (Recommended)

```bash
docker-compose up -d db
```

### Or Install PostgreSQL Locally

```bash
# Create database
createdb userdb
```

## Step 5: Run Migrations

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Run migrations
alembic upgrade head
```

## Step 6: Start Server

```bash
uvicorn app.main:app --reload
```

Output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

## Step 7: Test API

### Visit API Docs

Open browser: [http://localhost:8000/docs](http://localhost:8000/docs)

You'll see **Swagger UI** with all endpoints!

### Test Health Endpoint

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Register User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "name": "John Doe"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

## Step 8: Add Custom Endpoint

Let's add a user profile endpoint!

```bash
projex add endpoint profile --crud
```

This generates:
- `app/api/v1/endpoints/profile.py`
- Route handlers (GET, POST, PUT, DELETE)
- Tests

## Step 9: Add Model

```bash
projex add model Post --fields title:str,content:str,author_id:int
```

This creates:
- `app/models/post.py` - Database model
- `app/schemas/post.py` - Pydantic schemas
- Migration file

## Step 10: Run Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

Output:
```
=============== test session starts ===============
collected 12 items

tests/test_main.py ......                   [ 50%]
tests/api/test_users.py ......              [100%]

=============== 12 passed in 2.45s ===============
```

## Step 11: Deploy with Docker

```bash
# Build and run everything
docker-compose up --build

# Your API is now running in Docker!
```

## Step 12: Add CI/CD

```bash
projex add cicd --provider github
```

This creates `.github/workflows/ci.yml` with:
- Automated tests
- Linting
- Docker build
- Deployment ready

## Next Steps

### Enhance Your API

```bash
# Add more models
projex add model Comment --fields text:str,post_id:int

# Add services
projex add service email --async

# Add middleware
projex add middleware cors
```

### Add Documentation

```bash
projex add docs --tool mkdocs
mkdocs serve
```

### Environment Management

```bash
projex env add staging
projex env add production
```

### Code Quality

```bash
projex add quality-tools
pre-commit install
```

## Common Issues

### Database Connection Error

```bash
# Check DATABASE_URL in .env
# Ensure PostgreSQL is running
docker-compose up -d db
```

### Import Errors

```bash
# Activate virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use

```bash
# Use different port
uvicorn app.main:app --port 8001
```

## What You Learned

✅ Created a production-ready FastAPI project  
✅ Set up PostgreSQL database  
✅ Configured authentication  
✅ Added custom endpoints and models  
✅ Ran tests  
✅ Deployed with Docker  
✅ Set up CI/CD  

## Explore More

- [All Framework Templates](../templates/overview.md)
- [Smart Scaffolding Guide](../features/scaffolding.md)
- [Authentication Options](../features/authentication.md)
- [Database Configuration](../features/databases.md)