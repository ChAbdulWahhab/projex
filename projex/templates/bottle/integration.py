"""
Integration guide for Bottle welcome page.

- Serves the animated, responsive welcome template at '/'
- Keeps '/api' JSON response
"""

from bottle import Bottle, response
from pathlib import Path
import json

app = Bottle()
WELCOME_HTML = Path(__file__).with_name("welcome.html").read_text(encoding="utf-8")

@app.get('/')
def root():
    response.content_type = 'text/html; charset=UTF-8'
    return WELCOME_HTML

@app.get('/api')
def api_root():
    response.content_type = 'application/json'
    return json.dumps({"message": "Welcome to Bottle", "powered_by": "Projex CLI"})
