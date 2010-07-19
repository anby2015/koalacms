# Django settings for django_store project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os.path, sys
PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'payment_modules'))

ADMINS = (
    ('Albert Gazizov', 'deeper4k@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
import os
MEDIA_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media/')


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'zkpv2a7y5&jn3432+u(%wh&d6+ej^**c)#%_)l8cc=b=3n(2(ry'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'users.middleware.threadlocals.ThreadLocals',
)

ROOT_URLCONF = 'django_store.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)



INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'shop',
    'mptt',
    'mpttadmin',
    'webmoney',
    'prochange',
)

#Shop settings

SITE_PROTOCOL = 'http'
PAYMENT_MODULES = (
    'webmoney', 'prochange',            
)

#admin_tools setting
ADMIN_TOOLS_INDEX_DASHBOARD = 'admin_settings.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_THEMING_CSS = 'admin_tools/css/my_theming.css'

NEW_ORDERS_EXPIRED_TIME = 10
PRODUCTS_PER_PAGE = 4
PDORUCT_MAX_ORDER = 10
PRODUCT_CATEGORY_IMAGE = (30, 30, False) # resize image: True - with croping, False - without croping
PRODUCT_IMAGE_SIZE = (640, 480, False) # resize image: True - with croping, False - without croping
PRODUCT_COVER_SIZE = (300, 300, False) # creates a thumbnail: True - with croping, False - without croping
PRODUCT_THUMBNAIL_SIZE = (35, 35, True) # creates a thumbnail: True - with croping, False - without croping

