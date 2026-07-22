"""core URL configuration."""
from django.contrib import admin
from django.urls import path, include

from django.http import JsonResponse

urlpatterns = [
    path("", lambda request: JsonResponse({"status": "healthy", "message": "AI-First CRM HCP API is running"})),
    path("admin/", admin.site.urls),
    path("api/v1/hcp/", include("apps.hcp.urls")),
]
