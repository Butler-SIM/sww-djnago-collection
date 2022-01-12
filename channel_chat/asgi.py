"""
ASGI config for api_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django
from channels import *
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_server.settings.deploy")
django.setup()
application = get_default_application()