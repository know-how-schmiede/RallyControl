"""
ASGI config for rallycontrol project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

from django.core.asgi import get_asgi_application
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rallycontrol.settings")

application = get_asgi_application()
