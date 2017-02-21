"""
WSGI config for SQLweb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

from os import environ

environ["DJANGO_SETTINGS_MODULE"]="SQLweb.settings"

application = get_wsgi_application()
application = DjangoWhiteNoise(application)