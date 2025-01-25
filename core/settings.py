from pathlib import Path
from decouple import Config, RepositoryEnv

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

config = Config(RepositoryEnv('/app/.env'))

# Security settings
SECRET_KEY = config("DJANGO_SECRET")
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)

# GDAL and GEOS paths for spatial operations
GDAL_LIBRARY_PATH = "/lib/libgdal.so.30"
GEOS_LIBRARY_PATH = "/lib/aarch64-linux-gnu/libgeos_c.so"

# Allowed hosts
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="localhost").split(",")

# Installed apps
INSTALLED_APPS = [
    # Required for the backend
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",

    # GIS support
    "django.contrib.gis",

    # Custom apps
    "location",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

# URL Configuration
ROOT_URLCONF = "core.urls"

# WSGI application
WSGI_APPLICATION = "core.wsgi.application"

# Database settings
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB", default="app_database"),
        "USER": config("POSTGRES_USER", default="postgres"),
        "PASSWORD": config("POSTGRES_PASSWORD", default="password"),
        "HOST": config("POSTGRES_HOST", default="localhost"),
        "PORT": config("POSTGRES_PORT", default="5432"),
        "OPTIONS": {
            "options": "-c search_path=location_api"
        },
    }
}

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
