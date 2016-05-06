from .settings import *  # noqa

import os


DEBUG = False

ALLOWED_HOSTS = [
    os.environ["KEL_CLUSTER_API_HOST"]
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(levelname)s %(asctime)s %(module)s] %(message)s"
        },
        "simple": {
            "format": "%(levelname)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.environ["KEL_LOG_LEVEL"],
        },
        "kel.api": {
            "handlers": ["console"],
            "level": os.environ["KEL_LOG_LEVEL"],
        }
    }
}
