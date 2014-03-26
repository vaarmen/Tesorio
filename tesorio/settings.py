# Django settings for tesorio project.

import sys
import os
import random
try:
    import credentials
except:
    raise Exception('You need to create a credentials.py file in Tesorio/tesorio. ask Fabio')
sys.path.append('tesorio/deps')

# the below came from http://codespatter.com/2009/04/10/how-to-add-locations-to-python-path-for-reusable-django-apps/
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, PROJECT_ROOT)

DEBUG = not os.environ.get('SERVER_SOFTWARE', 'Development').startswith('Development')
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Fabio Fleitas', 'cubanfabio@gmail.com'),
    ('Carlos Vega', 'carlos@tesorio.com'),
)

# This is used for password_reset and other times django's internal send_mail is called
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = credentials.SENDGRID_USER
EMAIL_HOST_PASSWORD = credentials.SENDGRID_PASS
EMAIL_PORT = 587
EMAIL_USE_TLS = True

MANAGERS = ADMINS

# from http://stackoverflow.com/questions/1400529/does-google-app-engine-with-app-engine-patch-support-emailing-admins-upon-500-er
SERVER_EMAIL = 'carlos@tesorio.com'
# for password_reset
DEFAULT_FROM_EMAIL = SERVER_EMAIL
# from comment in http://stackoverflow.com/a/4180124/
EMAIL_BACKEND = 'appengine_emailbackend.EmailBackend'

GRAPPELLI_ADMIN_TITLE = 'Tesorio'

if not DEBUG:
    try:
        # Probably in appengine development server, otherwise manage.py shell
        app_id = environ['APPLICATION_ID']
    except:
        # from http://einaregilsson.com/unit-testing-model-classes-in-google-app-engine/
        # environ['APPLICATION_ID'] = 'dev~emeraldexam'
        # datastore_file = '/dev/null'
        # from google.appengine.api import apiproxy_stub_map,datastore_file_stub
        # apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
        # stub = datastore_file_stub.DatastoreFileStub('dev~emeraldexam', datastore_file, '/')
        # apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)

        # from above, in the comments...
        from google.appengine.ext import testbed
        t = testbed.Testbed()
        t.activate()
        t.init_datastore_v3_stub()


    from local_settings import DATABASE_NAME, DATABASE_USER
    # from http://www.joemartaganna.com/web-development/running-django-13-in-google-app-engine-with-google-cloud-sql/
    # print 'in DEBUG MODE'
    # sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/MySQL_python-1.2.4-py2.7.egg-info')
    # print sys.path
    SOUTH_DATABASE_ADAPTERS = {
        'default': "south.db.mysql"
    }
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DATABASE_NAME,
            'USER': DATABASE_USER,
            'HOST': '127.0.0.1', # needed for windows
            'PORT': '3306', # needed for windows
        }
    }
else:
    # print 'NOT in DEBUG mode'
    DATABASE_INSTANCE = 'tesorio-company:tesorio-sql-2' # Looks like 'apiproject:sampleinstance'
    DATABASE_NAME = 'tesoriodb2'
    BASE_URL = 'https://www.tesorio.com'
    SOUTH_DATABASE_ADAPTERS = {'default': 'south.db.mysql'}
    DATABASES = {
        'default': {
            'ENGINE': 'google.appengine.ext.django.backends.rdbms',
            'INSTANCE': DATABASE_INSTANCE,
            'NAME': DATABASE_NAME,
        }
    }


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    '.tesorio.com',
    '.tesorio-company.appspot.com',
    # try uncommenting the below if you run into problems when running DEBUG=False on localhost.
    'localhost:8080',
    'localhost'
]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

LOGIN_URL = '/login/'  # default is /accounts/login/
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/dashboard/'

# this is for setting how long a session cookie is active by default
SESSION_COOKIE_AGE = 3600 * 2  # 2h
SESSION_COOKIE_SECURE = False  # change this when switched over to https
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(
    os.path.dirname(__file__), 'tesorio', 'media'
).replace('\\', '/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = 'static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '44(ef9ea3e=lsj8j065#73hp8jiq13&%kyi92*2a@*5s7+usew'

# List of callables that know how to import templates from various sources.
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# #     'django.template.loaders.eggs.Loader',
# )
TEMPLATE_LOADERS = (
    'django_jinja.loaders.AppLoader',
    'django_jinja.loaders.FileSystemLoader',
)
DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.jinja'


# only use the memory file uploader,
# do not use the file system - not able to do so on
# google app engine
# credit: http://stackoverflow.com/a/4319384/1048433
FILE_UPLOAD_HANDLERS = ('django.core.files.uploadhandler.MemoryFileUploadHandler',)
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # the django default: 2.5MB


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tesorio.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'tesorio.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(
        os.path.dirname(__file__), 'tesorio', 'templates'
    ).replace('\\', '/'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (

    # third parties that must be loaded first
    'longerusername',  # From https://github.com/GoodCloud/django-longer-username
    'grappelli',

    # other third parties
    'django.contrib.humanize',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',

    # third party apps
    # 'password_reset',
    'south',
    'django_jinja',
    'simple_history',
    'bootstrap3',

    # tesorio apps
    'app',
    'tesorio',

)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
