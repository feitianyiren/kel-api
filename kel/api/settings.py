import os

import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = "changeme"
ROOT_URLCONF = "kel.api.urls"
WSGI_APPLICATION = "kel.api.wsgi.application"
DATABASES = {
    "default": dj_database_url.config(default="postgres://localhost/kel")
}
MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware"
]
INSTALLED_APPS = [
    "pinax.api",
    "kel.api",
]
KEL = {
    "IDENTITY_URL": os.environ["KEL_IDENTITY_URL"]
}
