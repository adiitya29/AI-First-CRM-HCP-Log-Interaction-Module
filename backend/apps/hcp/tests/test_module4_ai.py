"""
Tests for Module 4: LangGraph AI Agent for parsing natural language interactions.
We use `unittest.mock.patch` to mock the agent's response to avoid making real 
network calls to the Groq API during testing.
"""
import json
from unittest.mock import patch
import pytest
from django.urls import reverse

from apps.hcp.ai.schemas import InteractionExtraction


@pytest.mark.django_db
class TestAIChatView:
    url = reverse("hcp:chat")

    def test_chat_requires_message(self, client):
        response = client.post(self.url, data={}, content_type="application/json")
        assert response.status_code == 400

    @patch("apps.hcp.views.parse_interaction_text")
    def test_chat_returns_structured_data(self, mock_parse, client):
        # Setup mock return value
        mock_parse.return_value = {
            "hcp_name": "Dr. Sharma",
            "interaction_type": "in_person",
            "date": "2026-07-17",
            "notes": "Discussed CardioPlus with Dr. Sharma.",
            "products_discussed": ["CardioPlus"],
            "follow_up_required": True,
            "follow_up_date": "2026-07-24",
            "ai_summary": "In-person visit with Dr. Sharma discussing CardioPlus.",
            "ai_sentiment": "positive"
        }

        payload = {"message": "I met with Dr. Sharma today to discuss CardioPlus. I will follow up next week."}
        response = client.post(self.url, data=json.dumps(payload), content_type="application/json")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
        parsed = data["parsed_data"]
        assert parsed["hcp_name"] == "Dr. Sharma"
        assert parsed["interaction_type"] == "in_person"
        assert "CardioPlus" in parsed["products_discussed"]
        assert parsed["follow_up_required"] is True

    @patch("apps.hcp.views.parse_interaction_text")
    def test_chat_handles_agent_error(self, mock_parse, client):
        # Setup mock error
        mock_parse.return_value = {"error": "Groq API rate limit exceeded."}

        payload = {"message": "Test error handling"}
        response = client.post(self.url, data=json.dumps(payload), content_type="application/json")
        
        assert response.status_code == 500
        data = response.json()
        assert "error" in data
        assert data["error"] == "Groq API rate limit exceeded."
