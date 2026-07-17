"""
Test-specific Django settings.
Always uses SQLite in-memory — never touches Supabase.
Inherits all other settings from development.
"""
from .development import *  # noqa: F401, F403

# Force in-memory SQLite regardless of DATABASE_URL in .env
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
