"""
WSGI config for hellodjango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os, sys
sys.path.append('/home/pi/hellodjango')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hellodjango.settings")

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()
