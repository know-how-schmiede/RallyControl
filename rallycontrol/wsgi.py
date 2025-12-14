"""
WSGI config for rallycontrol project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rallycontrol.settings")

application = get_wsgi_application()
