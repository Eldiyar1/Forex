import os
from pathlib import Path
from .env_reader import env
from datetime import timedelta
from .jazzmin import *

# BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Production
PRODUCTION = env('PRODUCTION', default=False, cast=bool)

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THEME_APPS = ['jazzmin']

LIBRARY_APPS = [
    'rest_framework',
    'corsheaders',
    'django_filters',
    "rest_framework_simplejwt",
    'debug_toolbar',
    'drf_yasg',
    "phonenumber_field",
]

LOCAL_APPS = [
    'apps.common.apps.CommonConfig',
    'apps.users.apps.UsersConfig',
    'apps.courses.apps.CoursesConfig',
]

INSTALLED_APPS = [
    *THEME_APPS,
    *DJANGO_APPS,
    *LIBRARY_APPS,
    *LOCAL_APPS
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "pretty": {
            "format": "\033[1;36m{levelname}\033[0m \033[1;34m{asctime}\033[0m \033[1m{module}\033[0m {message}",
            "style": "{",
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "email_backend": "django.core.mail.backends.filebased.EmailBackend",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "pretty",
            "level": "INFO",
        },
        "error_file": {
            "class": "logging.FileHandler",
            "filename": f"{BASE_DIR}/errors.log",
            "level": "ERROR",
            "formatter": "verbose",
        },
        "warning_file": {
            "class": "logging.FileHandler",
            "filename": f"{BASE_DIR}/warnings.log",
            "level": "WARNING",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "error_file", "warning_file"],
        "level": "DEBUG",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "error_file", "warning_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

ROOT_URLCONF = "cors.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cors.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

AUTH_USER_MODEL = "users.User"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": env("SECRET_KEY"),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
}

LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_L10N = True

USE_TZ = True

gettext = lambda s: s

LANGUAGES = [
    ('ru', gettext('Русский')),
    ('en', gettext('English')),
    ('kk', gettext('Қазақша')),
]

LOCALE_PATHS = [
    f"{BASE_DIR}/common/locale",
    f"{BASE_DIR}/courses/locale",
    f"{BASE_DIR}/users/locale",
    f"{BASE_DIR}/cors/locale",
]


# Static files
STATIC_URL = '/back_static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'back_static')

# Media files
MEDIA_URL = "/back_media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'back_media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATE_INPUT_FORMATS = [
    "%d.%m.%Y",
]

REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%d.%m.%Y %H:%M:%S",
    'DATE_FORMAT': "%d.%m.%Y",
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 13,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
}

if not PRODUCTION:
    from .local import *
else:
    from .production import *

if DEBUG:
    INTERNAL_IPS = ['127.0.0.1']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
