from pathlib import Path
import os
from datetime import timedelta
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "twitter-clone-ghw9.onrender.com",   
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",

    "accounts.apps.AccountsConfig",
    "users",
    "follows",
    "likes",
    "comments",
    "posts",
]

AUTH_USER_MODEL = "accounts.User"

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

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = "backend.urls"

DATABASES = {
    "default": dj_database_url.config(default="sqlite:///db.sqlite3")
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
