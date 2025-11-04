# Framework Templates Overview

Projex supports **8 production-ready Python frameworks**. Choose the one that fits your needs!

## Quick Comparison

| Framework | Type | Performance | Use Case | Learning Curve |
|-----------|------|-------------|----------|----------------|
| **FastAPI** | Async API | ⚡⚡⚡⚡⚡ | Modern APIs | Easy |
| **Django** | Full-Stack | ⚡⚡⚡ | Web Apps | Medium |
| **Flask** | Micro | ⚡⚡⚡⚡ | Simple APIs | Easy |
| **Bottle** | Micro | ⚡⚡⚡⚡ | Small Services | Very Easy |
| **Pyramid** | Flexible | ⚡⚡⚡ | Large Apps | Medium |
| **Tornado** | Async | ⚡⚡⚡⚡⚡ | Real-time | Medium |
| **Sanic** | Async | ⚡⚡⚡⚡⚡ | High-perf APIs | Easy |
| **CherryPy** | Minimal | ⚡⚡⚡ | Embedded Apps | Easy |

## Framework Selection Guide

### Choose FastAPI if you want:
- ✅ Modern async/await syntax
- ✅ Automatic API documentation
- ✅ Type hints and validation
- ✅ High performance
- ✅ WebSocket support

```bash
projex create my-api --template fastapi
```

[Read FastAPI Guide →](fastapi.md)

---

### Choose Django if you want:
- ✅ Batteries-included framework
- ✅ Built-in admin panel
- ✅ ORM with migrations
- ✅ Authentication system
- ✅ Large ecosystem

```bash
projex create my-site --template django
```

[Read Django Guide →](django.md)

---

### Choose Flask if you want:
- ✅ Lightweight and flexible
- ✅ Minimal boilerplate
- ✅ Easy to learn
- ✅ Great for APIs
- ✅ Extensive extensions

```bash
projex create my-app --template flask
```

[Read Flask Guide →](flask.md)

---

### Choose Bottle if you want:
- ✅ Single file framework
- ✅ No dependencies
- ✅ Ultra lightweight
- ✅ Quick prototyping
- ✅ Embedded applications

```bash
projex create my-service --template bottle
```

[Read Bottle Guide →](bottle.md)

---

### Choose Pyramid if you want:
- ✅ Flexibility and scalability
- ✅ Large application support
- ✅ Multiple database support
- ✅ Extensible architecture
- ✅ URL generation

```bash
projex create my-app --template pyramid
```

[Read Pyramid Guide →](pyramid.md)

---

### Choose Tornado if you want:
- ✅ Non-blocking I/O
- ✅ WebSocket support
- ✅ Long-polling
- ✅ High concurrency
- ✅ Real-time features

```bash
projex create my-realtime --template tornado
```

[Read Tornado Guide →](tornado.md)

---

### Choose Sanic if you want:
- ✅ Blazing fast performance
- ✅ Async/await everywhere
- ✅ Simple routing
- ✅ Middleware support
- ✅ WebSocket support

```bash
projex create my-fast-api --template sanic
```

[Read Sanic Guide →](sanic.md)

---

### Choose CherryPy if you want:
- ✅ Object-oriented approach
- ✅ Built-in tools
- ✅ Thread-pooled server
- ✅ Production ready
- ✅ Simple and clean

```bash
projex create my-server --template cherrypy
```

[Read CherryPy Guide →](cherrypy.md)

---

## All Templates Include

Every framework template comes with:

✅ **Docker Support** - Dockerfile and docker-compose  
✅ **Database Integration** - ORM/ODM configured  
✅ **Testing Setup** - pytest with examples  
✅ **Environment Config** - .env file management  
✅ **CORS Support** - Cross-origin configured  
✅ **Best Practices** - Industry-standard structure  
✅ **Documentation** - README with instructions  

## Template Styles

Each framework supports 3 template styles:

### Minimal
```bash
projex create my-app --template fastapi --style minimal
```
- Basic structure only
- No Docker
- Quick setup
- Perfect for learning

### Standard (Default)
```bash
projex create my-app --template fastapi
```
- Complete structure
- Docker included
- Testing setup
- Production-ready

### Full
```bash
projex create my-app --template fastapi --style full
```
- Everything from Standard
- CI/CD configuration
- Documentation setup
- Enhanced testing
- Code quality tools

## Customization Options

All templates can be customized with:

### Database
```bash
--db postgresql|mysql|mongodb|sqlite|redis
```

### Authentication
```bash
--auth jwt|oauth2|apikey|basic
```

### License
```bash
--license mit|apache|gpl|bsd|unlicense
```

### Additional Options
```bash
--no-git        # Skip git initialization
--no-venv       # Skip virtual environment
--gitignore     # Custom gitignore templates
```

## Example Combinations

### Production API
```bash
projex create api \
  --template fastapi \
  --db postgresql \
  --auth jwt \
  --style full \
  --license mit
```

### Simple Microservice
```bash
projex create service \
  --template bottle \
  --db redis \
  --style minimal
```

### Full-Stack Web App
```bash
projex create webapp \
  --template django \
  --db mysql \
  --auth oauth2 \
  --style full
```

### Real-Time Service
```bash
projex create realtime \
  --template tornado \
  --db mongodb \
  --style standard
```

## Next Steps

Choose your framework and dive deeper:

- [FastAPI Guide](fastapi.md)
- [Django Guide](django.md)
- [Flask Guide](flask.md)
- [Bottle Guide](bottle.md)
- [Pyramid Guide](pyramid.md)
- [Tornado Guide](tornado.md)
- [Sanic Guide](sanic.md)
- [CherryPy Guide](cherrypy.md)

Or explore features:

- [Smart Scaffolding](../features/scaffolding.md)
- [Authentication Options](../features/authentication.md)
- [Database Support](../features/databases.md)