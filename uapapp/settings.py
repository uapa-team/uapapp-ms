"""
Django settings for uapapp project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+(ha#nd6^&@n^4d3)k9my0!zb32tmwcr$3!&ctznw-4b)b6%br'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

CORS_ORIGIN_WHITELIST = [
    "https://www.ingenieria.bogota.unal.edu.co",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

# Application definition

INSTALLED_APPS = [
    'uapapp_ms.apps.UapappMsConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'uapapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'uapapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DB_HOST = os.environ.get('UAPAPP_DB_HOST')
DB_PORT = os.environ.get('UAPAPP_DB_PORT')
DB_NAME = os.environ.get('UAPAPP_DB_NAME')
DB_USER = os.environ.get('UAPAPP_DB_USER')
DB_PASS = os.environ.get('UAPAPP_DB_PASS')

MAIN_DB_HOST = os.environ.get('MAIN_DB_HOST')
MAIN_DB_PORT = os.environ.get('MAIN_DB_PORT')
MAIN_DB_NAME = os.environ.get('MAIN_DB_NAME')
MAIN_DB_USER = os.environ.get('MAIN_DB_USER')
MAIN_DB_PASS = os.environ.get('MAIN_DB_PASS')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST':     DB_HOST,
        'PORT':     DB_PORT,
        'NAME':     DB_NAME,
        'USER':     DB_USER,
        'PASSWORD': DB_PASS,
    },
    'mainDB': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST':     MAIN_DB_HOST,
        'PORT':     MAIN_DB_PORT,
        'NAME':     MAIN_DB_NAME,
        'USER':     MAIN_DB_USER,
        'PASSWORD': MAIN_DB_PASS,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/public/'
