import os
from django.core.exceptions import ImproperlyConfigured
from .base import *

DEBUG = False

if SECRET_KEY == 'django-insecure-dev-only-change-me':
    raise ImproperlyConfigured('SECRET_KEY environment variable must be set in production.')

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')

# Support both DATABASE_URL (Render) and individual DB_* vars
_database_url = os.environ.get('DATABASE_URL')
if _database_url:
    import urllib.parse
    _db = urllib.parse.urlparse(_database_url)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': _db.path.lstrip('/'),
            'USER': _db.username,
            'PASSWORD': _db.password,
            'HOST': _db.hostname,
            'PORT': _db.port or 5432,
        }
    }
else:
    _missing = [v for v in ('DB_NAME', 'DB_USER', 'DB_PASSWORD') if not os.environ.get(v)]
    if _missing:
        raise ImproperlyConfigured(f"Missing database env vars: {', '.join(_missing)}")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASSWORD'],
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }

# Whitenoise — insert after SecurityMiddleware
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

# Persistent DB connections
CONN_MAX_AGE = 60

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')

_redis_url = os.environ.get('REDIS_URL')
if _redis_url:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': _redis_url,
            'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
        }
    }
# else: inherits locmem cache from base.py

# Tell Django the original request was HTTPS even though Render forwards it as HTTP
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# HTTPS / security
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

