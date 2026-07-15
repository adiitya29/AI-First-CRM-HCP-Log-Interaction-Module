"""AppConfig for the HCP module."""
from django.apps import AppConfig


class HcpConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.hcp"
    verbose_name = "Healthcare Professionals"
