"""
Integration guide for CherryPy welcome page.

- Serves HTML at '/'
- JSON at '/api'
"""

import cherrypy
from pathlib import Path
import json

WELCOME_HTML = Path(__file__).with_name("welcome.html").read_text(encoding="utf-8")

class Root:
    @cherrypy.expose
    def index(self):
        cherrypy.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        return WELCOME_HTML

    @cherrypy.expose
    def api(self):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps({"message": "Welcome to CherryPy", "powered_by": "Projex CLI"})

if __name__ == '__main__':
    cherrypy.quickstart(Root())
