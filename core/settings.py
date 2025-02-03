from pathlib import Path
from datetime import timedelta
from environs import Env

# Initialize environs
env = Env()
env.read_env()

# API Key for Google Maps
GOOGLE_MAPS_API_KEY = env.str("GOOGLE_MAPS_DIRECTIONS_API_KEY")
GOOGLE_MAPS_API_SECRET = env.str("GOOGLE_MAPS_DIRECTIONS_SECRET")

ZIPCODE_API_KEY = env.str("GOOGLE_MAPS_DIRECTIONS_SECRET")


# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = env.str("DJANGO_SECRET")
DEBUG = env.bool("DJANGO_DEBUG", default=True)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost"])

# GDAL and GEOS paths for spatial operations
GDAL_LIBRARY_PATH = "/lib/libgdal.so.30"
GEOS_LIBRARY_PATH = "/lib/aarch64-linux-gnu/libgeos_c.so"

# Installed apps
INSTALLED_APPS = [
    # Required for the backend
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "rest_framework",
    "drf_spectacular",
    # GIS support
    "django.contrib.gis",
    # Custom apps
    "location",
    "routing",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

# URL Configuration
ROOT_URLCONF = "core.urls"

# WSGI application
WSGI_APPLICATION = "core.wsgi.application"

# REST framework settings
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "location.authentication.CustomJWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# Simple JWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=300),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# Database settings
DATABASES = {
    "default": {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        "NAME": env.str("POSTGRES_DB", default="app_database"),
        "USER": env.str("POSTGRES_USER", default="postgres"),
        "PASSWORD": env.str("POSTGRES_PASSWORD", default="password"),
        "HOST": env.str("POSTGRES_HOST", default="localhost"),
        "PORT": env.int("POSTGRES_PORT", default=5432),
        "OPTIONS": {"options": "-c search_path=locations_api"},
    }
}

# API documentation settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Capsule Service API",
    "DESCRIPTION": "Documentation for Capsule Service API",
    "VERSION": "1.0.0",
}


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

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

KAFKA_TOPIC = env.str("KAFKA_TOPIC", default="default_topic")
KAFKA_SERVERS = env.list("KAFKA_SERVERS", default=["kafka:9092"])