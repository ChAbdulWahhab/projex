"""
Integration guide for Pyramid welcome page.

Add a root view returning the HTML and include in the router.
"""

from pathlib import Path
from pyramid.response import Response
from pyramid.config import Configurator

WELCOME_HTML = Path(__file__).with_name("welcome.html").read_text(encoding="utf-8")

def welcome_view(_request):
    return Response(WELCOME_HTML, content_type="text/html")


def main(global_config, **settings):  # Pyramid entry point
    config = Configurator(settings=settings)
    config.add_route('welcome', '/')
    config.add_view(welcome_view, route_name='welcome')
    return config.make_wsgi_app()
