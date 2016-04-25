"""
Production specific settings for troupon project.
"""

from .base import *
import dj_database_url
import os

APPLICATION_DIR = os.path.dirname(globals()['__file__'])

DEBUG = True

DATABASES = {
    'default': dj_database_url.config()
}

BOWER_COMPONENTS_ROOT = os.path.join(
    APPLICATION_DIR, '..', '..', 'static')

BOWER_PATH = '/app/node_modules/bower'



# Enable Connection Pooling
# DATABASES['default']['ENGINE'] = 'django_postgrespool'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']
