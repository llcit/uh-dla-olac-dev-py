# settings/prod.py

"""
This file should never be edited with production values. 
Instead, use it as a template for the actual production settings file 
that is NOT be versioned or placed in a repository.
"""

from .base import *

DEBUG = False

TEMPLATE_DEBUG = False

# ! DO NOT EDIT THIS ON LOCAL ENVIRONMENTS! MEANT FOR PRODUCTION (but we want it in the repo).
ALLOWED_HOSTS = ['*.yourhost.com']

# Append apps needed in production.
# (nothing needed at the moment that is not specified in base.py)
# INSTALLED_APPS += ('someapp',)

# ! SACRED -- DO NOT EDIT THIS ON LOCAL ENVIRONMENTS! MEANT FOR PRODUCTION (but we want it in the repo).

SECRET_KEY = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

MEDIA_URL = ''

STATIC_URL = ''

# END SACRED
