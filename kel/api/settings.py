import os

import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = True

ALLOWED_HOSTS = []

SECRET_KEY = os.environ["SECRET_KEY"]

ROOT_URLCONF = "kel.api.urls"

WSGI_APPLICATION = "kel.api.wsgi.application"

DATABASES = {
    "default": dj_database_url.config(default="postgres://localhost/kel")
}

MIDDLEWARE_CLASSES = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware"
]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",

    "pinax.api",

    "kel.api"
]

AUTH_USER_MODEL = "api.User"

KEL = {
    "IDENTITY_URL": os.environ["KEL_IDENTITY_URL"]
}
