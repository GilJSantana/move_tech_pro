import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-local-dev-key-change-me")
DEBUG = os.getenv("DEBUG", "true").lower() in {"1", "true", "yes", "on"}
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000").rstrip("/")

ALLOWED_HOSTS = [host.strip() for host in os.getenv("ALLOWED_HOSTS", "*").split(",") if host.strip()]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django.contrib.sessions",
    "django.contrib.messages",
    "ecommerce",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {}

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
