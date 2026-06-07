"""
Django settings for CleanMail by Samod.

All secrets and environment-specific values are read from environment variables.
Database URL is parsed via dj-database-url.
"""

import os
from pathlib import Path

import dj_database_url

# =============================================================================
# Paths
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# Security
# =============================================================================
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "change-me-in-production")

DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,clean.wearesamod.com",
).split(",")

CSRF_TRUSTED_ORIGINS = ["https://clean.wearesamod.com"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# =============================================================================
# Application definition
# =============================================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "corsheaders",
    # Local
    "core",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"

# =============================================================================
# Database — parsed from DATABASE_URL env var
# =============================================================================
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get(
            "DATABASE_URL",
            "postgres://cleanmail:cleanmail@localhost:5432/cleanmail",
        ),
        conn_max_age=600,
        conn_health_checks=True,
    ),
}

# =============================================================================
# Password validation (for Django admin users)
# =============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =============================================================================
# Internationalisation
# =============================================================================
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Santo_Domingo"
USE_I18N = True
USE_TZ = True

# =============================================================================
# Static files
# =============================================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# =============================================================================
# Default primary key field type
# =============================================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =============================================================================
# CORS
# =============================================================================
CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "https://clean.wearesamod.com",
).split(",")

CORS_ALLOW_CREDENTIALS = True

# =============================================================================
# Django REST Framework
# =============================================================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "core.auth_backend.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
    "EXCEPTION_HANDLER": "core.exceptions.custom_exception_handler",
}

# =============================================================================
# Redis
# =============================================================================
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

# =============================================================================
# JWT settings
# =============================================================================
JWT_SECRET = os.environ.get("JWT_SECRET", SECRET_KEY)
JWT_EXPIRATION_HOURS = int(os.environ.get("JWT_EXPIRATION_HOURS", "72"))

# =============================================================================
# n8n webhook URL for sending magic-link emails
# =============================================================================
N8N_MAGIC_LINK_WEBHOOK = os.environ.get("N8N_MAGIC_LINK_WEBHOOK", "")

# =============================================================================
# LemonSqueezy webhook secret for HMAC verification
# =============================================================================
LEMONSQUEEZY_WEBHOOK_SECRET = os.environ.get("LEMONSQUEEZY_WEBHOOK_SECRET", "")

# =============================================================================
# LemonSqueezy product-variant → credits mapping
# =============================================================================
LEMONSQUEEZY_VARIANT_CREDITS = {
    os.environ.get("LS_VARIANT_STARTER", "variant_starter"): 2000,
    os.environ.get("LS_VARIANT_PRO", "variant_pro"): 10000,
    os.environ.get("LS_VARIANT_AGENCY", "variant_agency"): 30000,
}

# =============================================================================
# Paddle webhook secret and price-ID → credits mapping
# =============================================================================
PADDLE_WEBHOOK_SECRET = os.environ.get("PADDLE_WEBHOOK_SECRET", "")

PADDLE_PRICE_CREDITS = {
    os.environ.get("PADDLE_PRICE_STARTER", "price_starter"): 2000,
    os.environ.get("PADDLE_PRICE_PRO", "price_pro"): 10000,
    os.environ.get("PADDLE_PRICE_AGENCY", "price_agency"): 30000,
}

# =============================================================================
# Frontend base URL (for magic-link generation)
# =============================================================================
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://clean.wearesamod.com")

# =============================================================================
# File upload max size (10 MB)
# =============================================================================
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
