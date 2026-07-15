"""
HCP module models – scaffold only.
Full models will be added in the next milestone.
"""
from django.db import models


# ---------------------------------------------------------------------------
# Placeholder – real models coming in Milestone 2
# ---------------------------------------------------------------------------
class HealthcareProfessional(models.Model):
    """Represents a Healthcare Professional (HCP) entity."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=200, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    institution = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "Healthcare Professional"
        verbose_name_plural = "Healthcare Professionals"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.specialty})"


class Interaction(models.Model):
    """Logs a field rep's interaction with an HCP."""

    class InteractionType(models.TextChoices):
        IN_PERSON = "in_person", "In-Person Visit"
        PHONE = "phone", "Phone Call"
        EMAIL = "email", "Email"
        VIRTUAL = "virtual", "Virtual Meeting"
        EVENT = "event", "Event / Conference"

    class LogMethod(models.TextChoices):
        FORM = "form", "Structured Form"
        CHAT = "chat", "Conversational Chat (AI)"

    hcp = models.ForeignKey(
        HealthcareProfessional,
        on_delete=models.CASCADE,
        related_name="interactions",
    )
    interaction_type = models.CharField(
        max_length=20,
        choices=InteractionType.choices,
        default=InteractionType.IN_PERSON,
    )
    log_method = models.CharField(
        max_length=10,
        choices=LogMethod.choices,
        default=LogMethod.FORM,
    )
    date = models.DateField()
    notes = models.TextField(blank=True)
    products_discussed = models.JSONField(default=list, blank=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)

    # AI-generated fields (populated by LangGraph agent)
    ai_summary = models.TextField(blank=True)
    ai_sentiment = models.CharField(max_length=50, blank=True)

    created_by = models.CharField(max_length=100, blank=True)  # rep identifier
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name = "Interaction"
        verbose_name_plural = "Interactions"

    def __str__(self):
        return f"{self.interaction_type} with {self.hcp} on {self.date}"
