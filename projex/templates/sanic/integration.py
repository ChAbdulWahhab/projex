"""
Integration guide for Sanic welcome page.

- Serves HTML at '/'
- JSON at '/api'
- Link users to Sanic docs; API explorer depends on chosen extensions
"""

from sanic import Sanic
from sanic.response import html, json
from pathlib import Path

app = Sanic("projex_sanic_app")
WELCOME_HTML = Path(__file__).with_name("welcome.html").read_text(encoding="utf-8")

@app.get("/")
async def root(_request):
    return html(WELCOME_HTML)

@app.get("/api")
async def api_root(_request):
    return json({"message": "Welcome to Sanic", "powered_by": "Projex CLI"})

# Optional: if using sanic-ext, you may enable OpenAPI and docs via configuration.
