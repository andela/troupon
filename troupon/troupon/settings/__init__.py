"""
Settings package initialization.
"""

import os

from .celery import app as celery_app
# Ensure development settings are not used in testing and production:
if not os.getenv('CI') and not os.getenv('HEROKU'):
    # load and set environment variables from '.env.yml' or '.env.py' files with django_envie
    from django_envie.workroom import convertfiletovars
    convertfiletovars()

    from development import *

if os.getenv('HEROKU') is not None:
    from production import *
