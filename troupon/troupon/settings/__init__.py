"""
Settings package initialization.
"""

import os

# Ensure development settings are not used in testing and production:
if not os.getenv('CI') and not os.getenv('HEROKU'):
    from development import *