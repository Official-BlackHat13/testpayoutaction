"""
Django settings for payout project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r0qb-hl8+la(qma%+fb2&)hd3ty9)0!l(gdtd_1l_y(sad-m6='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ["192.168.65.238","0.0.0.0","192.168.65.244","192.168.34.42","127.0.0.1","localhost","192.168.34.15","192.168.34.43","192.168.34.36"]
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    "corsheaders",
    "drf_yasg",
    "apis",
    "sabpaisa",
    "paytmchecksum",
    "ifaddr",
   
]
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOWED_ORIGIN_REGEXES=True
# CORS_ALLOWED_ORIGINS = [

# ]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    "auth-token",
    "auth_token",
    "Auth_token",
    
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "apis.middlewares.IpWhiteListed",
    "apis.middlewares.MultiTabsRestriction",
    "apis.middlewares.checkClientStatus"
]

ROOT_URLCONF = 'payout.urls'


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
REST_FRAMEWORK = { 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],}
WSGI_APPLICATION = 'payout.wsgi.application'
# CRONJOBS =[
#     # ("0 5 0 1/1 * ? *","apis.jobs.EnterDailyBalance"),
#     ("0 0/1 * 1/1 * ? *","apis.jobs.EnterDailyBalance"),
# ]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'u287339841_payout',
    #     'USER': 'u287339841_payout',
    #     'PASSWORD': 'Payout@123',
    #     'HOST': 'papernotes.in',
    #     'PORT': '3306',
    #     # 'socket': '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
    # }
    # Localdatabase

    #deployment db

    #  'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'payout_for_development',
    #     'USER': 'payout_for_development',
    #     'PASSWORD': 'payout@123',
    #     'HOST': 'localhost',
    #     'PORT': '3306',
    #     # 'socket': '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
    # }

    #  'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'payout_for_development',
    #     'USER': 'payout_for_development',
    #     'PASSWORD': 'payout@123',
    #     'HOST': 'localhost',
    #     'PORT': '3306',
    #     # 'socket': '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
    # }
    #  'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'stagingPayout',
    #     'USER': 'stagingPayout',
    #     'PASSWORD': 'ooTee0ie',
    #     'HOST': '172.16.157.5',
    #     'PORT': '3306',
    #     # 'socket': '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
    # }

     'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stagingPayout',
        'USER': 'stagingPayout',
        'PASSWORD': 'ooTee0ie',
        'HOST': '172.16.157.5',
        'PORT': '3306',
        # 'socket': '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
    }
    #  'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'stagingPayout',
    #     'USER': 'stagingPayout',
    #     'PASSWORD': 'ooTee0ie',
    #     'HOST': '172.16.157.5',
    #     'PORT': '3306',
    #     # 'socket': '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
    # }

    # kanishk local db
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'payout',
    #     'USER': 'root',
    #     'PASSWORD': 'root',
    #     'HOST': '127.0.0.1',
    #     'PORT': '3306',
    #     # 'socket': '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
    # }
    # yash local db
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'payout',
    #     'USER': 'root',
    #     'PASSWORD': 'DXZn*6!"n,YN!c8z',
    #     'HOST': '127.0.0.1',
    #     'PORT': '3306',
    #     # 'socket': '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
    # }
    #kunal local db
    # 'default': {
    #      'ENGINE': 'django.db.backends.mysql',
    #      'NAME': 'payoutdb',
    #      'USER': 'root',
    #      'PASSWORD': "root",
    #      'HOST': "127.0.0.1",
    #      'PORT': "3306",
    #  }
}
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
