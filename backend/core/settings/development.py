"""Development settings – extends base."""
from .base import *  # noqa: F401, F403

DEBUG = True

# Allow all origins in dev for convenience
CORS_ALLOW_ALL_ORIGINS = True

# Detailed logging in development
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}
