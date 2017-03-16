"""
Django settings for freelancefinder application.

Requires django-environ
"""

import environ
# from . import VERSION
VERSION = '0.0.3'

root = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env(root('.env'))

BASE_DIR = root()

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

# TODO: Set this appropriately
ALLOWED_HOSTS = ['*']

PREREQ_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin',
    'allauth.socialaccount.providers.reddit',
    'django_logtail',
    'taggit',
]

if DEBUG:
    PREREQ_APPS += [
        'debug_toolbar',
    ]

PROJECT_APPS = [
    'jobs',
    'remotes',
    'users',
]

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS

# Enable allauth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

REDDIT_USER_AGENT = 'django:work.freelancefinder:{} (by /u/phile19_81)'.format(VERSION)
REDDIT_CLIENT_ID = env('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = env('REDDIT_CLIENT_SECRET')

# Configure allauth, no username
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
SITE_ID = 1

SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'github': {},
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
    'linkedin': {
        'SCOPE': ['r_emailaddress'],
        'PROFILE_FIELDS': ['id', 'first-name', 'last-name', 'email-address',
                           'picture-url', 'public-profile-url'],
    },
    'reddit': {
        'AUTH_PARAMS': {'duration': 'permanent'},
        'SCOPE': ['identity', 'submit'],
        'USER_AGENT': REDDIT_USER_AGENT,
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'freelancefinder.middleware.xforwardedfor.XForwardedForMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    INTERNAL_IPS = [
        '192.168.2.1',
        '192.168.2.2',
        '192.168.2.3',
        '192.168.2.4',
        '192.168.2.5',
    ]

ROOT_URLCONF = 'freelancefinder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

WSGI_APPLICATION = 'freelancefinder.wsgi.application'

DATABASES = {
    'default': env.db()
}

LOG_LEVEL = DEBUG == 'DEBUG' and 'DEBUG' or 'INFO'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        },
    },
    'formatters': {
        'main': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            # Since we're doing json logging, just throw everything in there
            'format': '''
                %(threadName)s %(name)s %(thread)d %(created)f
                %(process)d %(processName)s %(relativeCreated)f
                %(module)s %(funcName)s %(levelno)d %(msecs)f
                %(pathname)s %(lineno)d %(asctime)s %(message)s
                %(filename)s %(levelname)s %(request_id)s
            ''',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
        'celery': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            # Since we're doing json logging, just throw everything in there
            'format': '''
                %(threadName)s %(name)s %(thread)d %(created)f
                %(process)d %(processName)s %(relativeCreated)f
                %(module)s %(funcName)s %(levelno)d %(msecs)f
                %(pathname)s %(lineno)d %(asctime)s %(message)s
                %(filename)s %(levelname)s
            ''',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'email': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false', 'request_id'],
        },
        'logfile': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/freelancefinder.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'main',
            'filters': ['request_id'],
        },
        'celery': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/freelancefinder.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'celery',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'main',
            'filters': ['require_debug_true', 'request_id'],
        },
        'null': {
            "class": 'logging.NullHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['email', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['null', ],
        },
        'celery': {
            'handlers': ['console', 'celery'],
            'level': 'DEBUG',
        },
        'py.warnings': {
            'handlers': ['null', ],
        },
        '': {
            'handlers': ['console', 'logfile'],
            'level': "DEBUG",
        },
    }
}

# Logtail config
LOGTAIL_FILES = {
    'celery_beat': '/var/log/celery/beat.log',
    'celery_worker': '/var/log/celery/worker.log',
    'django': '/var/log/django/freelancefinder.log',
    'gunicorn_access': '/var/log/gunicorn/access.log',
    'gunicorn_error': '/var/log/gunicorn/error.log',
    'nginx_access': '/var/log/nginx/access.log',
    'nginx_error': '/var/log/nginx/error.log',
    'redis': '/var/log/redis/redis-server.log',
    'supervisord': '/var/log/supervisord/supervisord.log',
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

# Celery settings
CELERY_BROKER_URL = env('REDIS_CELERY_URL')
CELERY_RESULT_BACKEND = env('REDIS_CELERY_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS = ('remotes.tasks',)
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

public_root = root.path('public/')

MEDIA_ROOT = public_root('media')
MEDIA_URL = 'media/'

STATIC_ROOT = public_root('static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [root('static')]
