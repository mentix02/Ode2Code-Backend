import os
import decouple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    SECRET_KEY = decouple.config('SECRET_KEY')
except decouple.UndefinedValueError:
    print("SECRET_KEY not configured. Run `make` for configure settings.")
    exit(1)

try:
    DEBUG = decouple.config('DEBUG', cast=bool)
except decouple.UndefinedValueError:
    DEBUG = True

INTERNAL_IPS = ('127.0.0.1',)

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # local
    'core.apps.CoreConfig',
    'blog.apps.BlogConfig',
    'author.apps.AuthorConfig',
    'tutorial.apps.TutorialConfig',
    # third party
    'vote',
    'corsheaders',
    'debug_toolbar',
    'rest_framework',
    'drf_multiple_model',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'backend.wsgi.application'

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

try:
    USER = decouple.config('DB_USER')
    PASSWORD = decouple.config('DB_PASSWORD')
except decouple.UndefinedValueError:
    USER = ''
    PASSWORD = ''

DATABASES = {
    'default': {
        'HOST': '',
        'PORT': '',
        'USER': USER,
        'NAME': 'ode2code',
        'ENGINE': 'django.db.backends.mysql',
        'PASSWORD': PASSWORD,
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django.server': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# third party package configuration

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'PAGE_SIZE': 12,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# production settings
"""
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 60
CSRF_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
"""
