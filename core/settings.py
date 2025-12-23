# core/settings.py

from pathlib import Path
import os
import dj_database_url
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY ---
SECRET_KEY = config('SECRET_KEY', default='django-insecure-default-key-change-me')
DEBUG = config('DEBUG', default=False, cast=bool)

# Add your specific Railway domain here
ALLOWED_HOSTS = [
    'web-production-0ddd6.up.railway.app',
    'localhost',
    '127.0.0.1',
    '.railway.app',
]

# Required for Django 4.0+ to allow logins/POST requests on Railway
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-0ddd6.up.railway.app',
    'https://*.railway.app',
]

# --- PROXY SETTINGS (Crucial for 502/Redirect issues) ---
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --- APPS & MIDDLEWARE ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Best place for Whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- DATABASE ---
# Automatically uses Railway Postgres if available, else SQLite
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default=f"sqlite:///{BASE_DIR}/db.sqlite3"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# --- STATIC FILES (WhiteNoise) ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
# Production-ready storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- PRODUCTION SECURITY ---
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True