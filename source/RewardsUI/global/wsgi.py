# WSGI entry point used to serve the Django project from a production
# web server (the dev setup uses manage.py runserver instead).

"""
WSGI config for rewards project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "global.settings")

application = get_wsgi_application()
