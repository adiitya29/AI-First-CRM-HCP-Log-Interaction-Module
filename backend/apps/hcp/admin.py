"""
HCP module admin registrations – scaffold.
"""
from django.contrib import admin
from .models import HealthcareProfessional, Interaction


@admin.register(HealthcareProfessional)
class HealthcareProfessionalAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "specialty", "institution", "email")
    search_fields = ("first_name", "last_name", "specialty", "institution")
    ordering = ("last_name", "first_name")


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ("hcp", "interaction_type", "log_method", "date", "follow_up_required")
    list_filter = ("interaction_type", "log_method", "follow_up_required")
    search_fields = ("hcp__first_name", "hcp__last_name", "notes")
    ordering = ("-date",)
