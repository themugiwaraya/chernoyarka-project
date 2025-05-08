"""
WSGI config for recreation_booking project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recreation_booking.settings')

application = get_wsgi_application()

if os.environ.get("RENDER", "") == "true":
    import pathlib
    exec(open(pathlib.Path(__file__).parent / "createsu.py").read())

