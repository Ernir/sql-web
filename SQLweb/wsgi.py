"""
WSGI config for SQLweb project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

from django.core.wsgi import get_wsgi_application

from os import environ

environ["DJANGO_SETTINGS_MODULE"]="SQLweb.settings"

application = get_wsgi_application()