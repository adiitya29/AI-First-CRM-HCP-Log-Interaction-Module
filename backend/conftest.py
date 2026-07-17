"""
conftest.py — Project-level pytest configuration.
Forces SQLite for all tests so they never touch the real Supabase DB.
"""
import django
from django.conf import settings


def pytest_configure(config):
    """Override DATABASE to use SQLite in-memory for all tests."""
    # Only override if not already set to sqlite
    if not getattr(settings, "DATABASES", {}).get("default", {}).get(
        "ENGINE", ""
    ).endswith("sqlite3"):
        settings.DATABASES["default"] = {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
