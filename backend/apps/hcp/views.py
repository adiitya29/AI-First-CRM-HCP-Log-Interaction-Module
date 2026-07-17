"""
HCP module views.
Provides REST API endpoints for HCPs and Interactions.
AI (LangGraph/Groq) will be wired in a later module.
"""
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import HealthcareProfessional, Interaction
from .serializers import (
    HealthcareProfessionalSerializer,
    InteractionSerializer,
    InteractionListSerializer,
)
from .ai.agent import parse_interaction_text


# ── Health Check ──────────────────────────────────────────────────────────────

def health_check(request):
    """Simple liveness probe – no auth required."""
    return JsonResponse({"status": "ok", "module": "hcp", "version": "0.1.0"})


# ── Healthcare Professional endpoints ─────────────────────────────────────────

class HCPListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/hcp/professionals/  → list all HCPs
    POST /api/v1/hcp/professionals/  → create a new HCP
    """
    queryset = HealthcareProfessional.objects.all()
    serializer_class = HealthcareProfessionalSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        # Optional query-param filtering
        specialty = self.request.query_params.get("specialty")
        search = self.request.query_params.get("search")
        if specialty:
            qs = qs.filter(specialty__icontains=specialty)
        if search:
            qs = qs.filter(
                first_name__icontains=search
            ) | qs.filter(
                last_name__icontains=search
            ) | qs.filter(
                institution__icontains=search
            )
        return qs


class HCPDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/v1/hcp/professionals/<pk>/  → retrieve
    PUT    /api/v1/hcp/professionals/<pk>/  → full update
    PATCH  /api/v1/hcp/professionals/<pk>/  → partial update
    DELETE /api/v1/hcp/professionals/<pk>/  → delete
    """
    queryset = HealthcareProfessional.objects.all()
    serializer_class = HealthcareProfessionalSerializer


# ── Interaction endpoints ─────────────────────────────────────────────────────

class InteractionListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/hcp/interactions/           → list all interactions
    GET  /api/v1/hcp/interactions/?hcp=<id>  → filter by HCP
    POST /api/v1/hcp/interactions/           → log a new interaction (form method)
    """
    queryset = Interaction.objects.select_related("hcp").all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return InteractionListSerializer
        return InteractionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        hcp_id = self.request.query_params.get("hcp")
        log_method = self.request.query_params.get("log_method")
        if hcp_id:
            qs = qs.filter(hcp_id=hcp_id)
        if log_method:
            qs = qs.filter(log_method=log_method)
        return qs


class InteractionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/v1/hcp/interactions/<pk>/  → retrieve
    PATCH  /api/v1/hcp/interactions/<pk>/  → partial update
    DELETE /api/v1/hcp/interactions/<pk>/  → delete
    """
    queryset = Interaction.objects.select_related("hcp").all()
    serializer_class = InteractionSerializer


# ── AI Chat (LangGraph + Groq) ───────────────────────────────────────────────

class ChatView(APIView):
    """
    POST /api/v1/hcp/chat/
    Accepts a natural-language message from the field rep and returns an
    AI-parsed interaction draft via the LangGraph agent.
    """

    def post(self, request):
        message = request.data.get("message", "").strip()
        if not message:
            return Response(
                {"error": "message field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Call the LangGraph agent to extract data
        parsed_data = parse_interaction_text(message)
        
        if "error" in parsed_data:
            return Response(
                {"error": parsed_data["error"]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "status": "success",
                "parsed_data": parsed_data,
            },
            status=status.HTTP_200_OK,
        )
