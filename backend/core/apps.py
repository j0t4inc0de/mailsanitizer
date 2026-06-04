"""App configuration for the core app — CleanMail by Samod."""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration for the core application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "CleanMail Core"
