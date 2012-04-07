# -*- coding: utf-8 -*-

"""

    readthedocs.settings.local
    ~~~~~~~~~~~~~~

    Short description of what's contained in the file

"""
from .base import *
import os.path


DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
    ('Full Name', 'email@domain.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'readthedocs',
        'USER': '', # Not used with sqlite3.
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}

REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    }

#MEDIA_URL = 'http://localhost/'
#ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    }

SLUMBER_USERNAME = 'test'
SLUMBER_PASSWORD = 'test'
SLUMBER_API_HOST = 'http://localhost:8000'


SESSION_COOKIE_DOMAIN = None
CACHE_BACKEND = 'dummy://'

TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_VERBOSE = True
TEST_OUTPUT_DESCRIPTIONS = True
TEST_OUTPUT_DIR = os.path.join(SITE_ROOT, 'xml_output')


