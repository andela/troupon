"""
 Django settings for troupon project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/

Defines settings that are common across deploys.
"""

from __future__ import absolute_import
import os
# from django_envie.workroom import convertfiletovars
import cloudinary

# load and set environment variables from '.env.yml'
# or '.env.py' files with django_envie
# convertfiletovars()

import datetime

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'djangobower',
    'django_nose',
    'djcelery',
    'allaccess',
    'haystack',
    'whoosh',
    'accounts',
    'authentication',
    'deals',
    'conversations',
    'merchant',
    'cart',
    'carton',
    'payment',
    'rest_framework',
    'rest_framework_swagger',
    'corsheaders',
    'django.contrib.sites',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'middleware.general.SharedContextMiddleware',
    'conversations.middleware.UnreadMessageCount',
)

ROOT_URLCONF = 'troupon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
            ],
        },
    },
]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken'
)

WSGI_APPLICATION = 'troupon.wsgi.application'

# Authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # Additional backend for allaccess
    'allaccess.backends.AuthorizedServiceBackend',
)

WHOOSH_INDEX = os.path.join(BASE_DIR, 'whoosh/')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': WHOOSH_INDEX,
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=18000),
}

# MEDIA_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# MEDIA_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

DEBUG = True

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'static')

BOWER_INSTALLED_APPS = (
    'jquery',
    'bootstrap',
    'fontawesome',
    'flickity',
    'packery',
)

# Cloudinary configuration handshake
cloudinary.config(cloud_name=os.getenv('cloudinary_cloud_name'),
                  api_key=os.getenv('cloudinary_api_key'),
                  api_secret=os.getenv('cloudinary_api_secret'))

# Image dimensions
SITE_IMAGES = {
    'slideshow_image_width': 1000,
    'slideshow_image_height': 1000,
    'thumbnail_image_width': 500,
    'thumbnail_image_height': 500
}

# deal listings and search:
DEALS = {
    'default_search_city': 25,
    'num_page_items': 15,
    'min_orphan_items': 2,
}

CART_PRODUCT_MODEL = 'deals.models.Deal'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NEXMO_USERNAME = os.getenv('NEXMO_USERNAME')
NEXMO_PASSWORD = os.getenv('NEXMO_PASSWORD')
NEXMO_FROM = 'Troupon'
OTP_SECRET_KEY = os.getenv('OTP_SECRET_KEY')
# Defined rabbitmq user
BROKER_URL = "amqp://1KSjqqZh:golZT1TcOxAA9yLvCISWzotedCoSvZ5N@white-bartsia-45.bigwig.lshift.net:10097/Mfp0HgAcgl9Q"
# Troupon's email
TROUPON_EMAIL = 'noreplytroupon@andela.com'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)
SITE_ID = 1
LOGIN_REDIRECT_URL = "/"
