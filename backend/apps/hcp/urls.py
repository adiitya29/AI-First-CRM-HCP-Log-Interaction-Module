"""
HCP module URL patterns.
"""
from django.urls import path
from . import views

app_name = "hcp"

urlpatterns = [
    # Liveness probe
    path("health/", views.health_check, name="health-check"),

    # Healthcare Professional CRUD
    path("professionals/", views.HCPListCreateView.as_view(), name="hcp-list-create"),
    path("professionals/<int:pk>/", views.HCPDetailView.as_view(), name="hcp-detail"),

    # Interaction CRUD
    path("interactions/", views.InteractionListCreateView.as_view(), name="interaction-list-create"),
    path("interactions/<int:pk>/", views.InteractionDetailView.as_view(), name="interaction-detail"),

    # AI Chat endpoint (stub → LangGraph agent in next module)
    path("chat/", views.ChatView.as_view(), name="chat"),
]
