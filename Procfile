web: python troupon/manage.py collectstatic --noinput --settings=troupon.settings.production --verbosity 0; gunicorn troupon.wsgi --pythonpath=troupon --log-file -
worker: python troupon/manage.py celery -A troupon worker -l info --beat -b
