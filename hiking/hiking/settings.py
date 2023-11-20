import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'some_default_key')

DEBUG = True

ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['45.12.73.72', 'hi-hiking.ru', '127.0.0.1', 'localhost']

CSRF_TRUSTED_ORIGINS = ['https://45.12.73.72', 'https://hi-hiking.ru', 'http://127.0.0.1', 'https://127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'trails.apps.TrailsConfig',
    'users.apps.UsersConfig',
    'about.apps.AboutConfig',
    'core.apps.CoreConfig',
    'django.contrib.postgres',
    'debug_toolbar',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'hiking.urls'

TEMPLATES_DIR = BASE_DIR / 'templates'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.regions.regions',
                'core.context_processors.settings_constants.constants',
            ],
        },
    },
]

WSGI_APPLICATION = 'hiking.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'postgres_db'),
        'USER': os.getenv('POSTGRES_USER', 'postgres_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres_password'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', 5432)
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR / 'static',)
# STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

COORDINATES_FORMAT = '^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'


LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'trails:index'
LOGOUT_REDIRECT_URL = 'trails:index'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'

CSRF_FAILURE_VIEW = 'core.views.csrf_failure'

INTERNAL_IPS = [
    '127.0.0.1',
]

AUTH_USER_MODEL = 'users.CustomUser'


# Constants
TRAILS_NUMBER_INDEX_PAGE = 8
TRAILS_NUMBER_REGION_PAGE = 8
TRAILS_NUMBER_ALL_TRAILS_PAGE = 12
TRAILS_NUMBER_TRAIL_PAGE = 4

COMMENTS_NUMBER_TRAIL_PAGE = 3
COMMENTS_NUMBER_COMMENTS_PAGE = 5

SITE_ID = 1