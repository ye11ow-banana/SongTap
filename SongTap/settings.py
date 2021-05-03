import datetime
import os
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(str(BASE_DIR.absolute()) + '/.env')

MY_DOMAIN = '159.89.15.53'

playlists_for_genres = {
    'common': 'pl.rp-L22YULVxawyR',
}

DEV_SECRET_KEY = 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjVaQzZNSjVDM1UifQ.eyJpc3MiOiJSUlpIUFFXSjVGIiwiaWF0IjoxNjExMTQ5NzI2LCJleHAiOjE2MjY5MTQxMjZ9._i_JvOOJpvIHwFJ2QjqmIseet0hIlYmJZQH3sKep92Ml170BGhuj1t97kJNS8sEzKXvgsPoG4B58FkpwbbRZHg'

headers = {
    'Authorization': 'Bearer ' f'{DEV_SECRET_KEY}',
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)

AUTH_USER_MODEL = 'accounts.AppUser'

INSTALLED_APPS = [
    'modeltranslation',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.apple',
    # 'allauth.socialaccount.providers.facebook',
    'rest_framework',
    'accounts.apps.AccountsConfig',
    'playlist.apps.PlaylistConfig',
    'recomendations.apps.RecomendationsConfig',
    'friends.apps.FriendsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SongTap.urls'

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

WSGI_APPLICATION = 'SongTap.wsgi.application'

LOG_DIR = str(BASE_DIR.absolute()) + '/logs/' + datetime.date.today().strftime('%d-%m-%Y')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[LINE:%(lineno)d]-%(levelname)s-%(threadName)s-%(asctime)s-%(module)s-%(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(message)s'
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',

            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': f"{LOG_DIR}/bot.log",
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,
        },
        'accounts': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'formatter': 'verbose'
        },
        'playlist': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'formatter': 'verbose'
        },
        'recomendations': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'formatter': 'verbose'
        },
    }
}

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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(str(BASE_DIR.absolute()) + '/static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

gettext = lambda s: s
LANGUAGES = (
    ('ru', gettext('Russia')),
    ('en', gettext('English'))
)

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50
}

REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_USERNAME = os.getenv("REDIS_USERNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/1'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/2'

try:
    from .local_settings import *
except ImportError:
    from .prod_settings import *
