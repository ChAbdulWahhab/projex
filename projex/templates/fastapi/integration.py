"""
Integration guide for FastAPI welcome page.

- Serves the animated, responsive welcome template at '/'
- Keeps '/api' JSON response
- Highlights interactive docs at '/docs' and '/redoc'
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path

app = FastAPI(title="My API", version="1.0.0")

# Load the bundled welcome.html (copied into generated project)
WELCOME_PATH = Path(__file__).with_name("welcome.html")
WELCOME_HTML = WELCOME_PATH.read_text(encoding="utf-8") if WELCOME_PATH.exists() else "<h1>Welcome</h1>"


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    return HTMLResponse(content=WELCOME_HTML, status_code=200)


@app.get("/api", response_class=JSONResponse)
async def api_root() -> JSONResponse:
    return JSONResponse(
        {
            "message": "Welcome to FastAPI",
            "docs": "/docs",
            "powered_by": "Projex CLI",
        }
    )


@app.get("/health", response_class=JSONResponse)
async def health() -> JSONResponse:
    return JSONResponse({"status": "healthy"})
