import os
from .development import *

if 'PYTHON_ENV' in os.environ and os.environ['PYTHON_ENV'] == 'production':
    from .production import *
