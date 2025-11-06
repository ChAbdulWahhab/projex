"""
Integration guide for Django welcome page.

- Serves the animated, responsive welcome template at '/'
- Keeps Django admin at '/admin'
"""

from pathlib import Path
from django.http import HttpResponse
from django.urls import path, include
from django.contrib import admin

WELCOME_HTML = Path(__file__).with_name("welcome.html").read_text(encoding="utf-8")

def welcome_view(_request):
    return HttpResponse(WELCOME_HTML)

urlpatterns = [
    path("", welcome_view, name="welcome"),
    path("admin/", admin.site.urls),
]
