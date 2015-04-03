# Parse database configuration from $DATABASE_URL
import dj_database_url
#import os
DATABASES['default'] =  dj_database_url.config()
#DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}
#print os.environ.get('LOCAL_DEV', False), "Alex!!!!"
#if bool(os.environ.get('LOCAL_DEV', False)):
#if not os.environ.has_key('DATABASE_URL'):
#    os.environ['DATABASE_URL'] = 'postgres://localhost'
#DATABASES = {'default': dj_database_url.config(default=os.environ['DATABASE_URL'])}

# Override DATABASES['default'] with your local database configuration

#try:
#  database_url = os.environ["DATABASE_URL"]
#except KeyError:
#  database_url = "file:///{}".format(os.path.join(BASE_DIR, 'db.sqlite3'))
#
#DATABASES = { 'default': dj_database_url.config() }
#
#DATABASES = {'default': dj_database_url.config(default='postgres://wcmikblybrgqbz:ZycOXg48gWJlRGR3MVFA9qGxvB@ec2-23-23-210-37.compute-1.amazonaws.com:5432/d3ibjjmjb9fqrm')}


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


