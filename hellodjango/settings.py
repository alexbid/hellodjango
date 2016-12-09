"""
Django settings for hellodjango project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
    '/var/www/static/',
#    os.path.join(BASE_DIR, '/staticfiles'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pres36m7pn(#gc_ho^jz*1ilephs#9gz4fp#2)^a5xcp7*=)lx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
#TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

print STATIC_ROOT, STATICFILES_FINDERS
print STATICFILES_DIRS

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'hellodjango',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hellodjango.urls'

WSGI_APPLICATION = 'hellodjango.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# # Allow all host hosts/domain names for this site
ALLOWED_HOSTS = ['*']

# Parse database configuration from $DATABASE_URL
import dj_database_url

#DATABASES = { 'default' : dj_database_url.config()}
#DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.postgresql_psycopg2",
#    }
#}
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'marketdb',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'awsuser',
            'PASSWORD': 'Newyork2012',
#            'HOST': 'awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
            'HOST': '52.37.59.37',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.

            'PORT': '5432',                      # Set to empty string for default.
        }
    }

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

from os.path import join
#TEMPLATE_DIRS = (
#                        #"/Users/alex/hellodjango/hellodjango/templates"
#						join(BASE_DIR,  'templates'),
#                    )
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
#            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.core.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
     },
]

## try to load local_settings.py if it exists
#try:
#  from local_settings import *
#except Exception as e:
#  pass
