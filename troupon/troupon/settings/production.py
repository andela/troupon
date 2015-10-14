"""
Production specific settings for troupon project.
"""

from .base import *
import dj_database_url


DEBUG = False

DATABASES = {
    'default': dj_database_url.config()
}

# Enable Connection Pooling
DATABASES['default']['ENGINE'] = 'django_postgrespool'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']
