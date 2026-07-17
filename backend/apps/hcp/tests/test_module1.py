"""
Tests for the HCP module – Module 1 (Models, Serializers, Views).
These tests run against the URL routing and serializer logic without
requiring a live database (using Django's test client + in-memory DB).
"""
import pytest
from django.urls import reverse, resolve
from apps.hcp.views import (
    HCPListCreateView,
    HCPDetailView,
    InteractionListCreateView,
    InteractionDetailView,
    ChatView,
)


# ── URL resolution tests ───────────────────────────────────────────────────────

class TestHCPURLs:
    def test_health_check_resolves(self):
        url = reverse("hcp:health-check")
        assert url == "/api/v1/hcp/health/"

    def test_professionals_list_url_resolves(self):
        url = reverse("hcp:hcp-list-create")
        assert url == "/api/v1/hcp/professionals/"
        assert resolve(url).func.view_class == HCPListCreateView

    def test_professionals_detail_url_resolves(self):
        url = reverse("hcp:hcp-detail", kwargs={"pk": 1})
        assert url == "/api/v1/hcp/professionals/1/"
        assert resolve(url).func.view_class == HCPDetailView

    def test_interactions_list_url_resolves(self):
        url = reverse("hcp:interaction-list-create")
        assert url == "/api/v1/hcp/interactions/"
        assert resolve(url).func.view_class == InteractionListCreateView

    def test_interactions_detail_url_resolves(self):
        url = reverse("hcp:interaction-detail", kwargs={"pk": 1})
        assert url == "/api/v1/hcp/interactions/1/"
        assert resolve(url).func.view_class == InteractionDetailView

    def test_chat_url_resolves(self):
        url = reverse("hcp:chat")
        assert url == "/api/v1/hcp/chat/"
        assert resolve(url).func.view_class == ChatView


# ── Health check view test ─────────────────────────────────────────────────────

@pytest.mark.django_db
class TestHealthCheck:
    def test_health_check_returns_200(self, client):
        url = reverse("hcp:health-check")
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["module"] == "hcp"


# ── Serializer unit tests ──────────────────────────────────────────────────────

@pytest.mark.django_db
class TestHCPSerializer:
    def test_full_name_field(self):
        from apps.hcp.models import HealthcareProfessional
        from apps.hcp.serializers import HealthcareProfessionalSerializer

        hcp = HealthcareProfessional(first_name="Jane", last_name="Doe", specialty="Cardiology")
        serializer = HealthcareProfessionalSerializer(hcp)
        assert serializer.data["full_name"] == "Jane Doe"

    def test_interaction_validation_followup(self):
        from apps.hcp.serializers import InteractionSerializer
        import datetime

        # follow_up_required=True but no follow_up_date → should fail
        data = {
            "hcp": 999,  # fake pk, just testing validation logic
            "interaction_type": "in_person",
            "log_method": "form",
            "date": str(datetime.date.today()),
            "follow_up_required": True,
            "follow_up_date": None,
        }
        serializer = InteractionSerializer(data=data)
        serializer.is_valid()  # will fail on hcp FK, but we test our custom validator separately
        # Custom validation: follow_up_required without follow_up_date
        from rest_framework import serializers as drf_serializers
        instance_serializer = InteractionSerializer()
        with pytest.raises(drf_serializers.ValidationError):
            instance_serializer.validate({"follow_up_required": True, "follow_up_date": None})
