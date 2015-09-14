# Production specific settings
import dj_database_url
DATABASES = {
    'default': dj_database_url.config()
}

# Enable Connection Pooling
DATABASES['default']['ENGINE'] = 'django_postgrespool'
