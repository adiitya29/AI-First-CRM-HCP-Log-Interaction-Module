"""core URL configuration."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # API v1 – HCP module (wired up in the next milestone)
    path("api/v1/hcp/", include("apps.hcp.urls")),
]
