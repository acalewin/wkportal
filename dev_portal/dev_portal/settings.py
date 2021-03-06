"""
Django settings for dev_portal project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import psycopg2

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# TODO: replace this with autogenerating key.
SECRET_KEY = '0)ib^q%%mha3l7nifrthw2k=1)yk4g*hn4d7&#@)&8!@y)u3lx'

# SECURITY WARNING: don't run with debug turned on in production!
# TODO: turn this off before deployment
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'links',
    #'user',
    'wanikani',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dev_portal.urls'

WSGI_APPLICATION = 'dev_portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
	'USER': 'django',
	'PASSWORD': 'DDmNANnpY7', 
        'NAME': 'wkportal',
	'HOST': '127.0.0.1'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/django/dev_portal/static/'


# Celery settings
# TODO: change this
BROKER_URL = 'amqp://wkuser:ilikepasswords@localhost//'
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend'
