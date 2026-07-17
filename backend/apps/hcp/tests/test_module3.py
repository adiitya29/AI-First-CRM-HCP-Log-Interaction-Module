"""
Module 3 — Full CRUD integration tests for the HCP API.
Covers: HCP endpoints, Interaction endpoints, filtering, validation.
"""
import datetime
import json
import pytest
from django.urls import reverse

from apps.hcp.models import HealthcareProfessional, Interaction
from apps.hcp.tests.factories import HealthcareProfessionalFactory, InteractionFactory


# ══════════════════════════════════════════════════════════════════════════════
# HCP — HealthcareProfessional CRUD
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
class TestHCPList:
    url = "/api/v1/hcp/professionals/"

    def test_list_returns_200(self, client):
        HealthcareProfessionalFactory.create_batch(3)
        response = client.get(self.url)
        assert response.status_code == 200

    def test_list_returns_all_hcps(self, client):
        HealthcareProfessionalFactory.create_batch(4)
        response = client.get(self.url)
        data = response.json()
        # Pagination: results key present
        assert "results" in data
        assert data["count"] == 4

    def test_list_empty_when_no_hcps(self, client):
        response = client.get(self.url)
        data = response.json()
        assert data["count"] == 0
        assert data["results"] == []

    def test_list_filter_by_specialty(self, client):
        HealthcareProfessionalFactory(specialty="Cardiology")
        HealthcareProfessionalFactory(specialty="Oncology")
        response = client.get(self.url + "?specialty=Cardiology")
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["specialty"] == "Cardiology"

    def test_list_search_by_name(self, client):
        HealthcareProfessionalFactory(first_name="Rajesh", last_name="Kumar")
        HealthcareProfessionalFactory(first_name="Priya", last_name="Singh")
        response = client.get(self.url + "?search=Rajesh")
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["first_name"] == "Rajesh"


@pytest.mark.django_db
class TestHCPCreate:
    url = "/api/v1/hcp/professionals/"

    def test_create_hcp_returns_201(self, client):
        payload = {
            "first_name": "Arjun",
            "last_name": "Sharma",
            "specialty": "Cardiology",
            "email": "arjun.sharma@aiims.in",
            "phone": "+91-9876543210",
            "institution": "AIIMS Delhi",
        }
        response = client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        assert response.status_code == 201

    def test_create_hcp_persists_to_db(self, client):
        payload = {
            "first_name": "Meera",
            "last_name": "Patel",
            "specialty": "Oncology",
            "email": "meera.patel@tata.com",
        }
        client.post(self.url, data=json.dumps(payload), content_type="application/json")
        assert HealthcareProfessional.objects.filter(email="meera.patel@tata.com").exists()

    def test_create_hcp_full_name_in_response(self, client):
        payload = {"first_name": "Vikram", "last_name": "Nair", "specialty": "Neurology"}
        response = client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        data = response.json()
        assert data["full_name"] == "Vikram Nair"

    def test_create_hcp_duplicate_email_fails(self, client):
        HealthcareProfessionalFactory(email="dup@test.com")
        payload = {"first_name": "A", "last_name": "B", "email": "dup@test.com"}
        response = client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        assert response.status_code == 400

    def test_create_hcp_missing_required_fields_fails(self, client):
        # first_name is required
        response = client.post(
            self.url,
            data=json.dumps({"last_name": "Only"}),
            content_type="application/json",
        )
        assert response.status_code == 400


@pytest.mark.django_db
class TestHCPDetail:
    def test_retrieve_hcp_returns_200(self, client):
        hcp = HealthcareProfessionalFactory()
        url = f"/api/v1/hcp/professionals/{hcp.pk}/"
        response = client.get(url)
        assert response.status_code == 200
        assert response.json()["id"] == hcp.pk

    def test_retrieve_nonexistent_hcp_returns_404(self, client):
        response = client.get("/api/v1/hcp/professionals/99999/")
        assert response.status_code == 404

    def test_partial_update_hcp(self, client):
        hcp = HealthcareProfessionalFactory(specialty="Cardiology")
        url = f"/api/v1/hcp/professionals/{hcp.pk}/"
        response = client.patch(
            url,
            data=json.dumps({"specialty": "Oncology"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        hcp.refresh_from_db()
        assert hcp.specialty == "Oncology"

    def test_delete_hcp(self, client):
        hcp = HealthcareProfessionalFactory()
        url = f"/api/v1/hcp/professionals/{hcp.pk}/"
        response = client.delete(url)
        assert response.status_code == 204
        assert not HealthcareProfessional.objects.filter(pk=hcp.pk).exists()


# ══════════════════════════════════════════════════════════════════════════════
# Interaction CRUD
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
class TestInteractionList:
    url = "/api/v1/hcp/interactions/"

    def test_list_returns_200(self, client):
        InteractionFactory.create_batch(3)
        response = client.get(self.url)
        assert response.status_code == 200

    def test_list_returns_all_interactions(self, client):
        InteractionFactory.create_batch(5)
        response = client.get(self.url)
        data = response.json()
        assert data["count"] == 5

    def test_filter_interactions_by_hcp(self, client):
        hcp1 = HealthcareProfessionalFactory()
        hcp2 = HealthcareProfessionalFactory()
        InteractionFactory.create_batch(2, hcp=hcp1)
        InteractionFactory(hcp=hcp2)
        response = client.get(self.url + f"?hcp={hcp1.pk}")
        data = response.json()
        assert data["count"] == 2

    def test_filter_interactions_by_log_method(self, client):
        InteractionFactory.create_batch(2, log_method=Interaction.LogMethod.FORM)
        InteractionFactory(log_method=Interaction.LogMethod.CHAT)
        response = client.get(self.url + "?log_method=form")
        data = response.json()
        assert data["count"] == 2

    def test_list_response_has_hcp_name_field(self, client):
        hcp = HealthcareProfessionalFactory(first_name="Test", last_name="Doc")
        InteractionFactory(hcp=hcp)
        response = client.get(self.url)
        data = response.json()
        assert "hcp_name" in data["results"][0]
        assert data["results"][0]["hcp_name"] == "Test Doc"


@pytest.mark.django_db
class TestInteractionCreate:
    url = "/api/v1/hcp/interactions/"

    def test_create_interaction_form_method(self, client):
        hcp = HealthcareProfessionalFactory()
        payload = {
            "hcp": hcp.pk,
            "interaction_type": "in_person",
            "log_method": "form",
            "date": str(datetime.date.today()),
            "notes": "Discussed new cardiology drug.",
            "products_discussed": ["CardioPlus"],
            "follow_up_required": False,
        }
        response = client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        assert response.status_code == 201

    def test_create_interaction_persists(self, client):
        hcp = HealthcareProfessionalFactory()
        payload = {
            "hcp": hcp.pk,
            "interaction_type": "phone",
            "log_method": "chat",
            "date": str(datetime.date.today()),
        }
        client.post(self.url, data=json.dumps(payload), content_type="application/json")
        assert Interaction.objects.filter(hcp=hcp, log_method="chat").exists()

    def test_create_requires_followup_date_when_flag_true(self, client):
        hcp = HealthcareProfessionalFactory()
        payload = {
            "hcp": hcp.pk,
            "interaction_type": "in_person",
            "log_method": "form",
            "date": str(datetime.date.today()),
            "follow_up_required": True,
            # follow_up_date intentionally missing
        }
        response = client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        assert response.status_code == 400
        assert "follow_up_date" in response.json()

    def test_create_with_followup_date_succeeds(self, client):
        hcp = HealthcareProfessionalFactory()
        payload = {
            "hcp": hcp.pk,
            "interaction_type": "in_person",
            "log_method": "form",
            "date": str(datetime.date.today()),
            "follow_up_required": True,
            "follow_up_date": str(datetime.date.today() + datetime.timedelta(days=7)),
        }
        response = client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        assert response.status_code == 201


@pytest.mark.django_db
class TestInteractionDetail:
    def test_retrieve_interaction(self, client):
        interaction = InteractionFactory()
        url = f"/api/v1/hcp/interactions/{interaction.pk}/"
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == interaction.pk
        # hcp_detail should be nested
        assert "hcp_detail" in data
        assert "full_name" in data["hcp_detail"]

    def test_retrieve_nonexistent_returns_404(self, client):
        response = client.get("/api/v1/hcp/interactions/99999/")
        assert response.status_code == 404

    def test_partial_update_interaction_notes(self, client):
        interaction = InteractionFactory(notes="Original notes")
        url = f"/api/v1/hcp/interactions/{interaction.pk}/"
        response = client.patch(
            url,
            data=json.dumps({"notes": "Updated notes after meeting"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        interaction.refresh_from_db()
        assert interaction.notes == "Updated notes after meeting"

    def test_delete_interaction(self, client):
        interaction = InteractionFactory()
        url = f"/api/v1/hcp/interactions/{interaction.pk}/"
        response = client.delete(url)
        assert response.status_code == 204
        assert not Interaction.objects.filter(pk=interaction.pk).exists()

    def test_ai_fields_are_read_only(self, client):
        """ai_summary and ai_sentiment should not be settable via API directly."""
        interaction = InteractionFactory(ai_summary="", ai_sentiment="")
        url = f"/api/v1/hcp/interactions/{interaction.pk}/"
        client.patch(
            url,
            data=json.dumps({"ai_summary": "Hacked summary", "ai_sentiment": "hacked"}),
            content_type="application/json",
        )
        interaction.refresh_from_db()
        # read_only fields must remain unchanged
        assert interaction.ai_summary == ""
        assert interaction.ai_sentiment == ""
