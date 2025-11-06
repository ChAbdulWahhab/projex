"""
Integration guide for Flask welcome page.

- Serves the animated, responsive welcome template at '/'
- Keeps '/api' JSON response
"""

from flask import Flask, Response, jsonify
from pathlib import Path

app = Flask(__name__)
WELCOME_HTML = Path(__file__).with_name("welcome.html").read_text(encoding="utf-8")


@app.get("/")
def root() -> Response:
    return Response(WELCOME_HTML, mimetype="text/html")


@app.get("/api")
def api_root():
    return jsonify({
        "message": "Welcome to Flask",
        "powered_by": "Projex CLI"
    })
