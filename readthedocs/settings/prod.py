from .base import *
import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG
TASTYPIE_FULL_DEBUG = True

DOMAIN = '<% HOST_IP %>'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'readthedocs',
        'USER': 'readthedocs_user',                      # Not used with sqlite3.
        'PASSWORD': 'readthedocs_pass_123',
        'HOST': 'localhost',  # assume mysql is installed locally
        'PORT': '3306',
        }
}
REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    }

# Add this in if you want email
#EMAIL_PORT = 25
#DEFAULT_FROM_EMAIL = ""
#SERVER_EMAIL = DEFAULT_FROM_EMAIL
#EMAIL_HOST = ''
#EMAIL_USE_TLS = False
#EMAIL_HOST_PASSWORD = ''
#EMAIL_HOST_USER = ''
#EMAIL_SUBJECT_PREFIX = 'RTFD'

MEDIA_URL = 'http://%s/' % DOMAIN #'http://<domain>/'
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'
#ADMIN_MEDIA_PREFIX = '/admin/'
INSTALLED_APPS.append('django.contrib.staticfiles')
STATIC_URL = 'http://%s/static' % DOMAIN #'http://<domain>/static'
# take from here
STATICFILES_DIRS = (
    str(SITE_ROOT+'/media'),
)
# put it here
STATIC_ROOT = '/opt/rtd/htdocs/static/'

CACHE_BACKEND = 'memcached://localhost:11211/'
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

HAYSTACK_CONNECTIONS = {
    'default': {
        #'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        #'URL': 'http://localhost:8983/solr',
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join('/opt/rtd/tmp', 'whoosh_index'),
        }
}
SLUMBER_USERNAME = 'test'
SLUMBER_PASSWORD = 'test'
SLUMBER_API_HOST = 'http://%s' % DOMAIN #'http://<domain>/'


SESSION_COOKIE_DOMAIN = None
CACHE_BACKEND = 'dummy://'

TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_VERBOSE = True
TEST_OUTPUT_DESCRIPTIONS = True
TEST_OUTPUT_DIR = os.path.join(SITE_ROOT, 'xml_output')

LOGS_ROOT="/opt/rtd/logs"
LOGGING['handlers']['logfile']['filename']=os.path.join(LOGS_ROOT, "rtd.log")
LOGGING['handlers']['errorlog']['filename']=os.path.join(LOGS_ROOT, "rtd.log")
LOGGING['handlers']['db']['filename']=os.path.join(LOGS_ROOT, "db.log")

# Everywhere is hardcoded with readthedocs.  We really want our domain here
SITE_DOMAIN=DOMAIN
