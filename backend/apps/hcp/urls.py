"""
HCP module URL patterns – scaffold only.
Real endpoints wired in the next milestone.
"""
from django.urls import path
from . import views

app_name = "hcp"

urlpatterns = [
    # Health-check endpoint (available immediately)
    path("health/", views.health_check, name="health-check"),

    # Interaction endpoints (stubbed – full implementation in Milestone 2)
    # path("interactions/", views.InteractionListCreateView.as_view(), name="interaction-list"),
    # path("interactions/<int:pk>/", views.InteractionDetailView.as_view(), name="interaction-detail"),
    # path("chat/", views.ChatView.as_view(), name="chat"),
]
