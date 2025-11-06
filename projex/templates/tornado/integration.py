"""
Integration guide for Tornado welcome page.

- Serves HTML at '/'
- Exposes JSON at '/api'
"""

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from pathlib import Path
import json

WELCOME_HTML = Path(__file__).with_name("welcome.html").read_text(encoding="utf-8")

class WelcomeHandler(RequestHandler):
    def get(self):
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.write(WELCOME_HTML)

class ApiHandler(RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps({"message": "Welcome to Tornado", "powered_by": "Projex CLI"}))


def make_app() -> Application:
    return Application([
        (r"/", WelcomeHandler),
        (r"/api", ApiHandler),
    ], debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    IOLoop.current().start()
