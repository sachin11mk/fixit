"""
Django settings for fixit project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'axg__p4v-z$7(-c#$*1-q^x)&x5*me4kqeknjzc9=ny^ag7^r_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

GOOGLE_OAUTH2_CLIENT_ID='1077258824046-lsb9thgrb61tlb0mamd2v4spaedvuot7.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET='9rNLn87nP8gkhi6qFr88sjLs'
#GOOGLE_OAUTH2_EXTRA_ARGUMENTS = {'hd': 'coriolis.co.in'}
#SOCIAL_AUTH_GoogleOAuth2Backend_WHITELISTED_DOMAINS = ['coriolis.co.in']
GOOGLE_WHITE_LISTED_DOMAINS = ['coriolis.co.in']
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
AUTHENTICATION_BACKENDS = (
   'social_auth.backends.google.GoogleOAuth2Backend',
   'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL          = '/login/google-oauth2/'
LOGIN_ERROR_URL    = '/task/list/'
LOGIN_REDIRECT_URL = "/task/list/"
SOCIAL_AUTH_LOGIN_REDIRECT_URL="/task/list/"


# Application definition

DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'social_auth',
)

CUSTOM_APPS = (
    'taskq',
    'admin_profile',
)

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'fixit.middleware.CustomSocialAuthExceptionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'fixit.urls'

WSGI_APPLICATION = 'fixit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'fixit.db'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_fixit',
        'USER': 'colama',
        'PASSWORD': 'coriolis',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False  #True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

BASE = os.path.abspath(os.path.dirname(__name__))

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

ADMIN_MEDIA_PREFIX = '/static/admin/'

TEMPLATE_DIRS = [ os.path.join(BASE_DIR, 'templates'), ]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
)


try:
    from local_settings import *
except:
    pass

